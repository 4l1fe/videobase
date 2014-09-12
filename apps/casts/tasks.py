# coding: utf-8

from operator import itemgetter

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from videobase.celery import app

from apps.casts.models import Casts, CastsLocations
from apps.casts.constants import APP_CASTS_MAIL_SUBJECT, APP_CASTS_MAIL_TEMPLATE


def find_min_price(price_list):
    has_free = min_obj = False

    for item in price_list:
        if item.price_type == 0:
            has_free = True
        else:
            if min_obj is False or min_obj.price > item.price:
                min_obj = item

    return has_free, min_obj


@app.task(name="cast_notify", queue="send_cast_notify")
def cast_notification(cast, user):
    o_user = User.objects.get(id=user)
    o_cast = Casts.objects.get(id=cast)

    o_loc = CastsLocations.objects.filter(cast=o_cast)
    has_free, min_obj = find_min_price(o_loc)

    context = {
        'cast': o_cast,
        'free': has_free,
        'min_obj': min_obj,
    }

    tpl = render_to_string(APP_CASTS_MAIL_TEMPLATE, context)
    msg = EmailMultiAlternatives(subject=APP_CASTS_MAIL_SUBJECT, to=o_user.email)
    msg.attach_alternative(tpl, 'text/html')
    msg.send()
