# coding: utf-8

from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from videobase.celery import app

from apps.casts.models import Casts, CastsLocations
from apps.casts.constants import APP_CASTS_MAIL_SUBJECT, APP_CASTS_MAIL_TEMPLATE

from apps.users.tasks import send_template_mail


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

    params = {
        'context': {
            'cast': model_to_dict(o_cast, fields=[field.name for field in o_cast._meta.fields]),
            'free': has_free,
            'min_obj': model_to_dict(min_obj, fields=[field.name for field in min_obj._meta.fields]),
        },
        'subject': APP_CASTS_MAIL_SUBJECT,
        'tpl_name': APP_CASTS_MAIL_TEMPLATE,
        'to': [o_user.email]
    }

    send_template_mail.s(kwargs=params).apply_async()
