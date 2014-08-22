# coding: utf-8

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from videobase.celery import app

from apps.films.models import Films
from apps.users.tasks import send_template_mail


@app.task(name="week_notification", queue="send_mail")
def best_of_the_best_this_week():
    o_films = Films.get_newest_films(limit=10)

    users = []
    for item in users:
        context = {
            'films': [],
            'serials': [],
            'streams': [],
        }

        params_email = {
            'subject': 'Newsletter',
            'tpl_name': 'newsletter.html',
            'to': item.email,
            'context': context,
        }

        send_template_mail.apply_async(kwargs=params_email)
