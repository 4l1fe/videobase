# coding: utf-8

import json
import zerorpc

from django.core.serializers.json import DjangoJSONEncoder

from apps.users.models import UsersPics
from utils.middlewares.local_thread import get_current_request


def render_page(page_type, context, use_req=True):
    data = {
        'template': page_type,
        'context': context,
    }

    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242", False)

    if use_req:
        request = get_current_request()
        if request.user.is_authenticated():
            user = request.user
            profile = user.profile
            data['context']['auth_user'] = {
                'id': user.id,
                'name': profile.get_name(),
                'avatar': UsersPics.get_picture(profile),
            }

    html = client.render(json.dumps(data, cls=DjangoJSONEncoder), async=False)
    client.close()

    return html
