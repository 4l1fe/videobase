# coding: utf-8

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from videobase.celery import app

from apps.casts.models import Casts, CastsLocations
from apps.casts.constants import APP_CASTS_MAIL_SUBJECT, APP_CASTS_MAIL_TEMPLATE


def find_min(price_list):
    free_view = False
    min_price = False

    min_value = min(price_list)
    if min_value > 0:
        min_price = min_value
        if price_list.index(min_value) > 0:
            free_view = True

    return free_view, min_price


@app.task(name="cast_notify", queue="send_cast_notify")
def cast_notification(cast, user):
    o_user = User.objects.get(id=user)
    o_cast = Casts.objects.get(id=cast)

    o_loc = CastsLocations.objects.raw(
        """
        SELECT DISTINCT ON (casts_locations.price) *
        FROM casts_locations
        WHERE casts_locations.cast_id = %s
        ORDER BY casts_locations.price LIMIT 2
        """, [o_cast.id]
    )

    price_list = [i.price for i in o_loc]
    free_view, min_price = find_min(price_list)

    context = {
        'cast': o_cast,
        'free': free_view,
        'min_price': min_price,
    }

    tpl = render_to_string(APP_CASTS_MAIL_TEMPLATE, context)
    msg = EmailMultiAlternatives(subject=APP_CASTS_MAIL_SUBJECT, to=o_user.email)
    msg.attach_alternative(tpl, 'text/html')
    msg.send()
