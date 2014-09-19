# coding: utf-8

from datetime import datetime, timedelta

from videobase.celery import app

from apps.films.models import Films
from apps.films.api.serializers import vbFilm
from apps.films.constants import APP_USERFILM_SUBS_TRUE, APP_FILMS_PERSON_SUB_EMAIL, APP_FILMS_WEEK_SUB_EMAIL

from apps.users.models import User, Feed, UsersRels
from apps.users.tasks import send_template_mail
from apps.users.api.serializers import vbFeedElement
from apps.users.constants import APP_USERPROFILE_NOTIFICATION_WEEK, APP_USERPROFILE_NOTIFICATION_DAY, \
    FILM_RATE, FILM_SUBSCRIBE, FILM_COMMENT

from apps.casts.models import Casts
from apps.casts.api.serializers import vbCast


@app.task(name="week_newsletter", queue="week_newsletter")
def best_of_the_best_this_week():
    curr_dt = datetime.now()

    # Выборка фильмов
    new_films = Films.get_newest_films(limit=10)
    new_films = vbFilm(new_films, many=True).data

    # Выборка сериалов
    serials = []

    # Основные параметры рассылки и контекст
    params_email = {
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
    o_users = User.objects.filter(
        email__isnull=False,
        profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_WEEK,
        profile__confirm_email=True,
    ).prefetch_related('profile__user')

    # Вычисляем воскресенье вечер
    start_dt = curr_dt - timedelta(days=7)
    end_dt = curr_dt + timedelta(days=6 - curr_dt.weekday())
    end_dt.replace(hour=23, minute=59, second=59)

    # Вставка параметров трансляции
    params_email['context']['casts']['old'] = vbCast(Casts.best_old_casts(start_dt=start_dt, end_dt=curr_dt), many=True).data,
    params_email['context']['casts']['future'] = vbCast(Casts.best_future_casts(start_dt=curr_dt, end_dt=end_dt), many=True).data,

    for item in o_users:
        params_email.update({'to': item.email})

        # Отправляем email в очередь
        send_template_mail.s(kwargs=params_email).apply_async()


@app.task(name="personal_newsletter", queue="personal_newsletter")
def personal_newsletter():
    # Основные параметры рассылки и контекст
    params_email = {
        'subject': APP_FILMS_PERSON_SUB_EMAIL,
        'tpl_name': u'mail/personal_newsletter.html',
        'context': {},
    }

    # Все пользователи у которых есть email и выбрана недельная рассылка
    o_users = User.objects.filter(
        email__isnull=False,
        profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_DAY,
        profile__confirm_email=True,
    ).prefetch_related('profile__user')

    for item in o_users:
        # Init data
        feeds = []

        # Выборка ленты друзей
        user_friends = UsersRels.get_all_friends_user(user_id=item.id, flat=True)

        # Проверка длинны
        if len(user_friends):
            # Собираем типы фидов из профиля
            type_film_feed = []

            if item.profile.ntf_frnd_rate:
                type_film_feed.append(FILM_RATE)

            if item.profile.ntf_frnd_comment:
                type_film_feed.append(FILM_COMMENT)

            if item.profile.ntf_frnd_subscribe:
                type_film_feed.append(FILM_SUBSCRIBE)

            if len(type_film_feed):
                feeds = Feed.objects.filter(user__in=user_friends, type__in=type_film_feed)
                feeds = vbFeedElement(feeds, many=True).data

        # Выборка фильмов
        films = Films.objects.filter(uf_films_rel__user=item.id, uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)

        # Проверка длинны
        if len(films):
            films = vbFilm(films, many=True).data
        else:
            films = []

        # Update
        params_email['to'] = item.email
        params_email['context'] = {
            'feeds': feeds,
            'films': films,
        }

        # Отправляем email в очередь
        send_template_mail.s(kwargs=params_email).apply_async()
