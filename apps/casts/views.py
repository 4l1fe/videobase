# coding: utf-8
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.utils import timezone
from utils.noderender import render_page

import apps.casts.models as casts_models
from apps.casts.api.serializers import vbCast
from apps.users.api.serializers import vbUser


class CastsView(View):

    def get(self, *args, **kwargs):
        today = timezone.datetime.now()
        data = {}
        casts = casts_models.Casts.objects.filter(start__gte=today - timezone.timedelta(hours=3)).order_by('start')[:12]
        data['casts'] = vbCast(casts).data
        data['casts_tags'] = []
        return HttpResponse(render_page('casts_list', data))


class CastInfoView(View):

    def get(self, request, cast_id, *args, **kwargs):
        today = timezone.datetime.now()
        data = {}

        try:
            cast = casts_models.Casts.objects.get(id=cast_id)
        except casts_models.Casts.DoesNotExist:
            raise Http404

        if request.user.is_authenticated():
            ccu, created = casts_models.CastsChatsUsers.objects.get_or_create(cast_id=cast_id, user_id=request.user.id)
            ccu.status = 'online'
            ccu.save()

        chat_items = casts_models.CastsChatsMsgs.objects.filter(cast_id=cast_id).iterator()
        msgs_list = []
        for item in chat_items:
            msgs_list.append({'user': vbUser(item.user).data, 'text': item.text})
        other_casts = casts_models.Casts.objects.filter(start__gte=today - timezone.timedelta(hours=3)).order_by('start').exclude(id=cast_id)[:12]
        data['cast'] = vbCast(cast).data
        data['cast']['chat_items'] = msgs_list
        data['online_casts'] = vbCast(other_casts, many=True).data
        return HttpResponse(render_page('cast', data))