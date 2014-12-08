# coding: utf-8

import sys
import traceback
from time import time

from django.db import connection, transaction
from django.core.management.base import BaseCommand

from apps.films.models import Films

from utils.common import dict_fetch_all


class Command(BaseCommand):

    help = u"Обсчет локального и консолидированного рейтинга"
    requires_model_validation = True

    step_limit = 200

    def handle(self, *args, **options):
        main_time = time()
        print u"Start calculate rating...."

        print u"Start calculate local ratings"
        self.calculate_local_rating()

        # Вычисляем консолидированный рейтинг
        # В случае медленного исполнения можно обсчитать в пуле тредов.
        # Батчи для этого уже сделаны.
        count_films = Films.objects.count()
        for index, offset in enumerate(xrange(0, count_films, self.step_limit), start=1):
            start = time()

            try:
                self.calc_our_ratings_for_chunk(offset)
            except Exception, e:
                self.print_error(e)

            print u"Elapsed time: {0}, Chunk: {1}".format(time() - start, index * self.step_limit)

        print u"Total Elapsed time: {0}".format(time() - main_time)

    @transaction.commit_on_success
    def calc_our_ratings_for_chunk(self, offset):
        def calc_rating_sort(instance):
            """
            Вычисление условного рейтинга для сортировки
            """

            rating_sort = instance.get_sort_cnt(instance.rating_cons_cnt) * \
                          instance.get_time_factor * instance.rating_cons

            return rating_sort

        # Выборка фильмов
        o_film = Films.objects.order_by('id')[offset:offset + self.step_limit]

        for item in o_film:
            # Calculate count consolidate rating
            item.rating_cons_cnt = item.get_calc_rating_cons_cnt

            # Calculate consolidate rating
            item.rating_cons = item.get_calc_rating_cons

            # Calculate rating sort
            item.rating_sort = calc_rating_sort(item)

            item.save()

    def calculate_local_rating(self):
        """
        Вычисление локального рейтинга
        """

        cursor = connection.cursor()
        try:
            query = """
                SELECT "users_films"."film_id", COALESCE(SUM("users_films"."rating"), 0) AS sum_films,
                COALESCE(COUNT("users_films"."film_id"), 0) AS count_films
                FROM "users_films" GROUP BY "users_films"."film_id" ORDER BY "users_films"."film_id"
            """

            cursor.execute(query)
            o_count = dict_fetch_all(cursor)

            # Обновляем локальные рейтинги
            self.update_local_params(o_count)

        except Exception, e:
            self.print_error(e)
            sys.exit(1)
        finally:
            cursor.close()

        print u"End calculate local ratings"

    @transaction.commit_on_success
    def update_local_params(self, items):
        # Сброс рейтингов
        Films.objects.update(rating_local_cnt=0, rating_local=0)

        for item in items:
            sum_value = 0

            if item['count_films']:
                sum_value = round(item['sum_films'] / item['count_films'], 1)

            # Обновляем локальный рейтинг
            Films.objects.filter(id=item['film_id']).\
                update(rating_local_cnt=item['count_films'], rating_local=sum_value)

    def print_error(self, e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace_msg = u''.join(traceback.format_tb(exc_traceback))

        error_msg = u"=============================\n"
        error_msg += u"Error: %s\n" % e
        error_msg += u"=============================\n"
        error_msg += u"Traceback:\n%s\n" % trace_msg
        error_msg += u"=============================\n"

        print error_msg
