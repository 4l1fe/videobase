# coding: utf-8

import math

from django.contrib.auth.models import User

from videobase.celery import app

from apps.casts.api.serializers import vbCast
from apps.casts.models import Casts, CastsLocations
from apps.casts.constants import APP_CASTS_MAIL_SUBJECT, APP_CASTS_MAIL_TEMPLATE

from apps.users.tasks import send_template_mail


def find_min_price(price_list):
    loc_cnt = 0
    has_free = min_obj = False

    for item in price_list:
        if item.price_type == 0:
            has_free = True
        else:
            loc_cnt += 1
            if min_obj is False or min_obj.price > item.price:
                min_obj = item

    return has_free, min_obj, loc_cnt


@app.task(name="cast_notify", queue="send_cast_notify")
def cast_notification(cast, user):
    o_user = User.objects.get(id=user)
    o_cast = Casts.objects.get(id=cast)

    o_loc = CastsLocations.objects.filter(cast=o_cast)
    has_free, min_obj, loc_cnt = find_min_price(o_loc)
    min_price = math.floor(min_obj.price) if min_obj else False

    params = {
        'context': {
            'cast': vbCast(o_cast, many=False).data,
            'free': has_free,
            'min_price': min_price,
            'loc_cnt': loc_cnt,
        },
        'subject': APP_CASTS_MAIL_SUBJECT,
        'tpl_name': APP_CASTS_MAIL_TEMPLATE,
        'to': [o_user.email],
    }

    send_template_mail.s(**params).apply()
