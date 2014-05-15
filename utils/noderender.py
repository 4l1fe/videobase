# coding: utf-8

import json
from subprocess import PIPE, Popen

from django.core.serializers.json import DjangoJSONEncoder


def render_page(page_type, context):
    encoder = DjangoJSONEncoder
    data = {
        'template': page_type,
        'context': context,
    }
    render_proc = Popen(['nodejs', 'renderproc.js'], stdin=PIPE, stdout=PIPE)

    html, status = render_proc.communicate(json.dumps(data, cls=encoder))
    return html