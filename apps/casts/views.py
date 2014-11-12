# coding: utf-8
from django.views.generic import View
from django.http import HttpResponse
from django.utils import timezone
from utils.noderender import render_page

import apps.casts.models as casts_models
from apps.casts.api.serializers import vbCast


class CastsView(View):

    def get(self, *args, **kwargs):
        today = timezone.datetime.now()
        data = {}
        casts = casts_models.Casts.objects.filter(start__gte=today - timezone.timedelta(hours=3)).order_by('start')[:12]
        data['casts'] = vbCast(casts, many=True).data
        data['casts_tags'] = []
        return HttpResponse(render_page('casts_list', data))


class CastInfoView(View):

    def get(self, *args, **kwargs):
        cast_id = int(kwargs.get('cast_id', None))
        today = timezone.datetime.now()
        data = {}
        cast = casts_models.Casts.objects.get(id=cast_id)
        chat_items = casts_models.CastsChatsMsgs.objects.filter(cast_id=cast_id)
        msgs_list = []
        for item in chat_items:
            user = {'id': item.user.id, 'name': u' '.join([item.user.first_name, item.user.last_name]), 'avatar': ""}
            msgs_list.append({'user': user, 'text': item.text})
        other_casts = casts_models.Casts.objects.filter(start__gte=today - timezone.timedelta(hours=3)).order_by('start').exclude(id=cast_id)[:12]
        data['cast'] = vbCast(cast).data
        data['cast']['chat_items'] = msgs_list
        data['online_casts'] = vbCast(other_casts, many=True).data
        return HttpResponse(render_page('cast', data))