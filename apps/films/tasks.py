# coding: utf-8

from videobase.celery import app

from apps.films.models import Films
from apps.films.api.serializers import vbFilm

from apps.users.models import User
from apps.users.tasks import send_template_mail
from apps.users.constants import APP_USERPROFILE_NOTIFICATION_WEEK, APP_USERPROFILE_NOTIFICATION_DAY


@app.task(name="week_notification", queue="week_notification")
def best_of_the_best_this_week():
    # Выборка фильмов
    o_films = Films.get_newest_films(limit=10)
    films = vbFilm(o_films).data

    # Выборка сериалов
    serials = []

    # Выборка трансляций
    streams = []

    # Основные параметры рассылки и контекст
    params_email = {
        'subject': 'Eженедельная рассылка ВсеВи',
        'tpl_name': 'newsletter.html',
        'context': {
            'films': films,
            'serials': serials,
            'streams': streams,
        },
    }

    # Все пользователи у которых есть email и выбрана недельная нотификация
    o_users = User.objects.filter(
        email__isnull=False,
        profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_WEEK
    )

    for item in o_users:
        params_email.update({'to': item.email})

        # Отправляем email в очередь
        send_template_mail.apply_async(kwargs=params_email)


@app.task(name="personal_notification", queue="personal_notification")
def personal_notification():
    # Выборка ленты друзей
    friend_feeds = []

    # Выборка сериалов
    films = []

    # Основные параметры рассылки и контекст
    params_email = {
        'subject': 'Персональная рассылка ВсеВи',
        'tpl_name': 'personal_newsletter.html',
        'context': {
            'feeds': friend_feeds,
            'films': films,
        },
    }

    # Все пользователи у которых есть email и выбрана недельная нотификация
    o_users = User.objects.filter(
        email__isnull=False,
        profile__ntf_frequency=APP_USERPROFILE_NOTIFICATION_DAY
    )

    for item in o_users:
        params_email.update({'to': item.email})

        # Отправляем email в очередь
        send_template_mail.apply_async(kwargs=params_email)
