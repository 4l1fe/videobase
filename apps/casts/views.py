# coding: utf-8
from django.http import HttpResponse, Http404
from utils.noderender import render_page

from apps.casts.api.list import CastsListView
from apps.casts.api.extras import CastsExtraView
from apps.casts.api.info import CastsInfoView
from apps.casts.api.serializers import vbCast

def casts_list_view(request):
    data = {
        'casts': get_casts(request),
    }
    return HttpResponse(render_page('casts_list', data))

def cast_view(request):
    casts = get_casts(request)

    data = {
        'cast': casts[0],
        'online_casts': casts,
    }
    return HttpResponse(render_page('cast', data))


def get_casts(request):
    try:
        o_casts = CastsListView.as_view()(request).data
        o_casts = o_casts['items']
        for o_cast in o_casts:
            o_cast['pg_rating'] = '+16'
            o_cast['description'] = """Прямая трансляция"""
            o_cast['locations'] = [
                {'type': "", 'quality': "", 'price': 0, 'price_type': 0, 'value': "/casts/0"},
                {'type': "", 'quality': "hd", 'price': 9000, 'price_type': 0, 'value': "/casts/0"},
                {'type': "", 'quality': "fhd", 'price': 100500, 'price_type': 0, 'value': "/casts/2"}
            ]

    except Exception, e:
        o_casts = []

    return o_casts