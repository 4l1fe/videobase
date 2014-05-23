# coding: utf-8
import json
import zerorpc

from django.core.serializers.json import DjangoJSONEncoder


def render_page(page_type, context):
    data = {
        'template': page_type,
        'context': context,
    }
    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242", False)
    html = client.render(json.dumps(data, cls=DjangoJSONEncoder), async=False)
    client.close()
    return html