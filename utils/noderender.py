# coding: utf-8

import json
import zerorpc

from django.core.serializers.json import DjangoJSONEncoder
from utils.middlewares.local_thread import get_current_request


def render_page(page_type, context):
    data = {
        'template': page_type,
        'context': context,
    }

    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242", False)

    result = get_current_request()
    if result.user.is_authenticated():
        user = result.user
        data['context']['auth_user'] = {
            'id': user.id,
            'name': user.get_full_name(),
            'avatar': '',
        }

    html = client.render(json.dumps(data, cls=DjangoJSONEncoder), async=False)
    client.close()

    return html
