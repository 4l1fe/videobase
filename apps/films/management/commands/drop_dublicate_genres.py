# coding: utf-8

from django.db import connection
from django.core.management.base import BaseCommand

from apps.films.models import Genres


class Command(BaseCommand):

    def handle(self, *args, **options):
        bad_genres_list = Genres.objects.filter(id__gte=37).order_by('id')
        not_del_genres_list = []

        for item in bad_genres_list:
            dublicate_list = []

            # Find original genre
            try:
                orig_genre = Genres.objects.get(name=item.name.strip().lower(), id__lt=37)
            except Exception, e:
                print u"Not find ID: {0}".format(item.id)
                not_del_genres_list.append(item.id)

                continue

            sql = """
                SELECT * FROM films_genres WHERE genres_id IN ({0}) ORDER BY films_id, genres_id;
            """.format(','.join(str(i) for i in [orig_genre.id, item.id]))

            cursor = connection.cursor()
            try:
                # Detect dublicate
                prev = None
                cursor.execute(sql)
                rows = cursor.fetchall()

                for i in rows:
                    if not prev is None:
                        if prev[1] == i[1]:
                            dublicate_list.append(i[0])

                    prev = i

                # Update films genres
                sql = "UPDATE films_genres SET genres_id={0} WHERE genres_id={1}".format(orig_genre.id, item.id)

                if len(dublicate_list):
                    print "Find dublicate IDs: {0}".format(dublicate_list)
                    sql += " AND id NOT IN ({0})".format(','.join([str(i) for i in dublicate_list]))

                cursor.execute(sql)

                # Drop dublicate
                sql = "DELETE FROM films_genres WHERE id IN ({0})".format(','.join([str(i) for i in dublicate_list]))
                cursor.execute(sql)

                # Drop genre
                Genres.objects.filter(id=item.id).delete()

            except Exception, e:
                print "ERROR: {0}".format(e)
            finally:
                cursor.close()
