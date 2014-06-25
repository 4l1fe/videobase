# coding: utf-8

import json
import zerorpc

from django.core.serializers.json import DjangoJSONEncoder
from utils.middlewares.local_thread import get_current_request
from apps.users.api.serializers import vbUser


def render_page(page_type, context):
    data = {
        'template': page_type,
        'context': context,
    }

    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242", False)

    request = get_current_request()
    if request.user.is_authenticated():
        data['context']['auth_user'] = vbUser(request.user).data

    html = client.render(json.dumps(data, cls=DjangoJSONEncoder), async=False)
    client.close()

    return html
