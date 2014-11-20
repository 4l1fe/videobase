# coding: utf-8

from datetime import datetime

from django.contrib.auth.models import User

from videobase.celery import app

from apps.casts.api.serializers import vbCast
from apps.casts.models import Casts
from apps.casts.constants import APP_CASTS_MAIL_SUBJECT, APP_CASTS_MAIL_TEMPLATE

from apps.users.tasks import send_template_mail


@app.task(name="cast_notification", queue="notify")
def cast_notification(cast, user, **kwargs):
    o_cast = Casts.objects.get(id=cast)

    if datetime.now() < o_cast.start:
        o_user = User.objects.get(id=user)
        vb_cast = vbCast(o_cast, many=False).data
        vb_cast['tag'] = vb_cast['tags'][0]['name'].capitalize()

        params = {
            'context': {
                'cast': vb_cast,
            },
            'subject': APP_CASTS_MAIL_SUBJECT,
            'tpl_name': APP_CASTS_MAIL_TEMPLATE,
            'to': [o_user.email],
            'jade_render': True,
        }

        send_template_mail.s(**params).apply_async()
    else:
        raise Exception('Истекло время')
