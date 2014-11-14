# coding: utf-8
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.utils import timezone
from utils.noderender import render_page
import apps.casts.models as casts_models
from apps.casts.api.serializers import vbCast
from apps.users.api.serializers import vbUser
from apps.casts.api import CastsListView


class CastsView(View):

    def get(self, *args, **kwargs):
        casts_tags_list = []

        tag_dict = {
            'id': '',
            'name': '',
            'type': ''
        }

        data = {}
        # Если пришли параметры то обратимся к API
        if len(self.request.REQUEST.keys()):
            api_resp = CastsListView().get(self.request)
            data['casts'] = api_resp.data['items']
        else:
            today = timezone.datetime.now()
            casts = casts_models.Casts.objects.filter(start__gte=today - timezone.timedelta(hours=3)).order_by('start')[:12]
            data['casts'] = vbCast(casts, many=True).data

        tags = casts_models.AbstractCastsTags.get_abstract_cast_tags()

        for tag in tags:
            tag_dict['id'] = tag.id
            tag_dict['name'] = tag.name
            tag_dict['type'] = tag.type
            casts_tags_list.append(tag_dict)

        data['casts_tags'] = casts_tags_list
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