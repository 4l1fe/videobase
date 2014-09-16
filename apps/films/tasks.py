# coding: utf-8

from django.db import connection, transaction

from videobase.celery import app

from apps.films.models import Films
from apps.films.constants import APP_USERFILM_SUBS_TRUE

from utils.common import dict_fetch_all


@app.task(name="calc_amount_subscribed_to_movie")
@transaction.commit_on_success
def calc_amount_subscribed_to_movie(*args, **kwargs):
    sql = """
    SELECT "users_films"."film_id", COUNT("users_films"."film_id") AS "film_cnt"
    FROM "users_films"
    WHERE "users_films"."subscribed" = %s
    GROUP BY "users_films"."film_id"
    ORDER BY "users_films"."film_id" ASC
    """

    cursor = connection.cursor()
    cursor.execute(sql, params=[APP_USERFILM_SUBS_TRUE])

    for item in dict_fetch_all(cursor):
        o_film = Films.objects.get(id=item['film_id'])

        o_film.subscribed_cnt = item['film_cnt']
        o_film.save()

    # Закрытие курсора
    cursor.close()
