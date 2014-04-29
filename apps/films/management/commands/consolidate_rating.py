# coding: utf-8

import sys
import datetime
import traceback

from time import time
from optparse import make_option

from django.db import connection
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from apps.films.models import Films, UsersFilms


class Command(BaseCommand):

    help = u'Обсчет локального и консолидированного рейтинга'
    requires_model_validation = True

    step_limit = 100

    def handle(self, *args, **options):
        main_time = time()
        print u"Start calculate rating...."

        # Вычисляем локальный рейтинг
        self.calculate_local_rating()

        # Вычисляем консолидированный рейтинг
        count_films = Films.objects.count()
        for index, offset in enumerate(xrange(0, count_films, self.step_limit), start=1):
            start = time()

            try:
                self.calc_our_ratings_for_chunk(offset)
            except Exception, e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                trace_msg = u''.join(traceback.format_tb(exc_traceback))

                error_msg = u"=============================\n"
                error_msg += u"Error: %s\n" % e
                error_msg += u"=============================\n"
                error_msg += u"Traceback:\n%s\n" % trace_msg
                error_msg += u"=============================\n"

                print error_msg

            print u"Elapsed time: {0}, Chunk: {1}".format(time() - start, index * self.step_limit)

        print u"Main Elapsed time: {0}".format(time() - main_time)


    @transaction.commit_on_success
    def calc_our_ratings_for_chunk(self, offset):
        # list_values = ['id', 'release_date', 'rating_local', 'rating_local_cnt', 'rating_imdb',
        #                'rating_imdb_cnt', 'rating_cons', 'rating_cons_cnt', 'rating_sort', 'kinopoisk_id'
        # ]
        # .values(*list_values)

        o_film = Films.objects.order_by('id')[offset:offset + self.step_limit]

        for item in o_film:
            rating_cons_cnt = self.calc_rating_cons_cnt(item)
            item.rating_cons_cnt = rating_cons_cnt

            rating_cons = self.calc_rating_cons(item)
            item.rating_cons = rating_cons

            rating_sort = self.calc_rating_sort(item)
            item.rating_sort = rating_sort

            item.save()


    def sort_cnt(self, rating_cons_cnt):
        """
            - если rating_cons_cnt больше 30 000, то sort_cnt = 5 000 + (sort_cnt - 30 000) / 150 + 15 000 / 50 + 10 000 / 20
            - если rating_cons_cnt больше 15 000, но меньше 30 000, sort_cnt = 5 000 + (rating_cons_cnt - 15000) / 50 + 10 000 / 20
            - если rating_cons_cnt больше 5 000, но меньше 15 000, то sort_cnt = 5 000 + (rating_cons_cnt - 5000) / 20
            - если rating_cons меньше или равно 5 000, то sort_cnt = rating_cons_cnt
        """

        if rating_cons_cnt > 30000:
            sort_cnt = 5000 + (rating_cons_cnt - 30000) / 150 + 15000 / 50 + 10000 / 20
        elif 15000 < rating_cons_cnt <= 30000:
            sort_cnt = 5000 + (rating_cons_cnt - 15000) / 50 + 10000 / 20
        elif 5000 < rating_cons_cnt <= 15000:
            sort_cnt = 5000 + (rating_cons_cnt - 5000) / 20
        else:
            sort_cnt = rating_cons_cnt

        return sort_cnt


    def time_factor(self, release_date):
        """
            - если release_date - текущая дата >= 700 дней, то time_factor = 1
            - если release_date - текущая дата < 700 дней, но больше 1, то time_factor = 1.5 - 0.5 * (release_date - текущая дата дней) / 700
            - если release_date - текущая дата <= 1, то time_factor = 1.5
        """
        days = (datetime.date.today() - release_date).days

        if days >= 700:
            time_factor = 1
        elif 1 < days < 700:
            time_factor = 1.5 - 0.5 * (-days) / 700
        else:
            time_factor = 1.5

        return time_factor


    def calculate_local_rating(self):
        """
            Вычисление локального рейтинга
        """

        cursor = connection.cursor()
        try:
            query = """
                SELECT "users_films"."film_id", COALESCE(SUM("users_films"."rating"), 0) AS sum_films,
                COALESCE(COUNT("users_films"."film_id"), 0) AS count_films
                FROM "users_films" GROUP BY "users_films"."film_id"
            """

            cursor.execute(query)
            desc = cursor.description
            o_count = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
        except Exception, e:
            pass
        finally:
            cursor.close()

        for item in o_count:
            sum = 0
            try:
                sum = item['count_films'] / item['sum_films']
            except:
                pass

            # Обновляем локальный рейтинг
            Films.objects.update(rating_local_cnt=item['count_films'], rating_local=sum)


    def calc_rating_cons_cnt(self, instance):
        """
            Высчитывается как сумма значений rating_local_cnt, rating_imdb_cnt, rating_kinopoisk_imdb
        """

        rating_local_cnt = instance.rating_local_cnt if not instance.rating_local_cnt is None else 0
        rating_imdb_cnt = instance.rating_imdb_cnt if not instance.rating_imdb_cnt is None else 0
        rating_kinopoisk_cnt = instance.rating_kinopoisk_cnt if not instance.rating_kinopoisk_cnt is None else 0

        return rating_local_cnt + rating_imdb_cnt + rating_kinopoisk_cnt


    def calc_rating_cons(self, instance):
        """
            Высчисление rating_cons по следующей формуле: 60% rating_kinopoisk + 30% rating_imdb + 10% rating_local.
            причём, если какое-то значение отсутствует или нулевое,
            то его доля распределяется между остальными значениями, например:
                - если rating_imdb не установлен, то формула становится 85.7% rating_kinpoisk + 14.3% rating_local
                - если rating_kinopoisk не установлен, то формула становится 75% rating_imdb + 25% rating_local
                - если rating_local не установлен, то формула становится 66.7% rating_kinopoisk + 33.3% rating_imdb
                - если rating_imdb и rating_kinopoisk не установлены, то формула становится 100% rating_local
        """

        values = ((6, instance.rating_kinopoisk), (3, instance.rating_imdb), (1, instance.rating_local),)
        divisor = float(sum(t[0] for t in values if t[1]))
        result = sum([t[0] / divisor * t[1] for t in values if t[1]])

        return result


    def calc_rating_sort(self, instance):
        """
            Вычисление условного рейтинга для сортировки
        """

        rating_sort = self.sort_cnt(instance.rating_cons_cnt) * \
                      self.time_factor(instance.release_date) * \
                      instance.rating_cons

        return rating_sort
