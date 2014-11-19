# coding: utf-8

import json

from datetime import datetime, timedelta
from django.db import connection, transaction
from django.core.serializers.json import DjangoJSONEncoder

from videobase import settings
from videobase.celery import app
from utils.common import dict_fetch_all

from apps.films.models import Films
from apps.films.api.serializers import vbFilm
from apps.films.constants import APP_USERFILM_SUBS_TRUE, APP_FILMS_PERSON_SUB_EMAIL, \
    APP_FILMS_WEEK_SUB_EMAIL

from apps.users.models import User, Feed, UsersRels
from apps.users.tasks import send_template_mail
from apps.users.api.serializers import vbFeedElement
from apps.users.constants import APP_USERPROFILE_NOTIFICATION_WEEK, APP_USERPROFILE_NOTIFICATION_DAY, \
    FILM_RATE, FILM_SUBSCRIBE, FILM_COMMENT, FILM_O

from apps.casts.models import Casts
from apps.casts.api.serializers import vbCast


@app.task(name="films.week_newsletter", queue="main")
def week_newsletter(*args, **kwargs):
    curr_dt = datetime.now()

    # Выборка фильмов
    new_films = Films.get_newest_films(limit=10)
    new_films = vbFilm(new_films, many=True, require_relation=False).data

    # Выборка сериалов
    serials = []

    # Основные параметры рассылки и контекст
    params_email = {
        'jade_render': True,
        'subject': APP_FILMS_WEEK_SUB_EMAIL,
        'tpl_name': 'week_newsletter',
        'context': {
            'films': new_films,
            'serials': serials,
            'casts': {
                'old': [],
                'future': [],
            },
        },
    }

    # Все пользователи у которых есть email и выбрана недельная нотификация
    o_users = User.objects.filter(is_staff=True).prefetch_related('profile__user')

    # .filter(
    #     email__isnull=False,
    #     profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_WEEK,
    #     profile__confirm_email=True,
    # ).prefetch_related('profile__user')

    # Вычисляем воскресенье вечер
    start_dt = curr_dt - timedelta(days=7)
    end_dt = curr_dt + timedelta(days=6 - curr_dt.weekday())
    end_dt.replace(hour=23, minute=59, second=59)

    # Вставка параметров трансляции
    params_email['context']['casts']['old'] = vbCast(Casts.best_old_casts(start_dt=start_dt, end_dt=curr_dt), many=True).data
    params_email['context']['casts']['future'] = vbCast(Casts.best_future_casts(start_dt=curr_dt, end_dt=end_dt), many=True).data

    if settings.DEBUG:
        data_json = json.dumps(params_email, cls=DjangoJSONEncoder)
        file = open('data.json', 'w')
        file.write(data_json)
        file.close()

    for item in o_users:
        params_email.update({'to': [item.email,]})

        # Отправляем email в очередь
        send_template_mail.s(**params_email).apply_async()


@app.task(name="films.personal_newsletter", queue="main")
def personal_newsletter(*args, **kwargs):
    curr_dt = datetime.now()
    start_dt = curr_dt - timedelta(days=1)

    # Основные параметры рассылки и контекст
    params_email = {
        'jade_render': True,
        'subject': APP_FILMS_PERSON_SUB_EMAIL,
        'tpl_name': 'personal_newsletter',
        'context': {
            'serials': [],
        },
    }

    # Все пользователи у которых есть email и выбрана недельная рассылка
    o_users = User.objects.filter(is_staff=True).prefetch_related('profile__user')

    # .filter(
    #     email__isnull=False,
    #     profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_DAY,
    #     profile__confirm_email=True,
    # ).prefetch_related('profile__user')

    for item in o_users:
        # Выборка ленты друзей
        user_friends = UsersRels.get_all_friends_user(user_id=item.id, flat=True)

        # Собираем типы фидов из профиля
        type_film_feed = [FILM_O]

        # Проверка длинны
        if len(user_friends):
            if item.profile.ntf_frnd_rate:
                type_film_feed.append(FILM_RATE)

            if item.profile.ntf_frnd_comment:
                type_film_feed.append(FILM_COMMENT)

            if item.profile.ntf_frnd_subscribe:
                type_film_feed.append(FILM_SUBSCRIBE)

        #
        ids = [item.id] + list(user_friends)

        # Выборка фильмов
        feeds = Feed.objects.\
            filter(user__in=ids, type__in=[FILM_O], created__gte=start_dt, created__lt=curr_dt).\
            order_by('created')

        if len(feeds):
            feeds = vbFeedElement(feeds, many=True).data

            # Update
            params_email['to'] = item.email
            params_email['context'] = {
                'feeds': feeds,
            }

            # Отправляем email в очередь
            send_template_mail.s(**params_email).apply_async()


@app.task(name="films.subscribed_to_movie", queue="main")
@transaction.commit_on_success
def calc_amount_subscribed_to_movie(*args, **kwargs):
    sql = """
    SELECT "users_films"."film_id", COUNT("users_films"."film_id") AS "film_cnt"
    FROM "users_films"
    WHERE "users_films"."subscribed" = %s
    GROUP BY "users_films"."film_id"
    ORDER BY "users_films"."film_id" ASC
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, params=[APP_USERFILM_SUBS_TRUE])

        for item in dict_fetch_all(cursor):
            o_film = Films.objects.get(id=item['film_id'])

            o_film.subscribed_cnt = item['film_cnt']
            o_film.save()
