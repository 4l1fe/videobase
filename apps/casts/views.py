# coding: utf-8
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.utils import timezone
from utils.noderender import render_page

import apps.casts.models as casts_models
from apps.casts.api.serializers import vbCast


class CastsView(View):

    def get(self, *args, **kwargs):
        today = timezone.datetime.now()
        data = {}
        casts = casts_models.Casts.objects.filter(start__gte=today.date()).order_by('start')[:12]
        data['casts'] = vbCast(casts).data
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
        other_casts = casts_models.Casts.objects.filter(start__gte=today.date()).order_by('start').exclude(id=cast_id)[:12]
        data['cast'] = vbCast(cast).data
        data['cast']['chat_items'] = msgs_list
        data['online_casts'] = vbCast(other_casts).data
        return HttpResponse(render_page('cast', data))

# def casts_list_view(request):
#     data = {
#         'casts': get_casts(request),
#     }
#     return HttpResponse(render_page('casts_list', data))
#
# def cast_view(request):
#     casts = get_casts(request)
#
#     data = {
#         'cast': casts[0],
#         'online_casts': casts,
#     }
#     return HttpResponse(render_page('cast', data))
#
#
# def get_casts(request):
#     try:
#         o_casts = CastsListView.as_view()(request).data
#         o_casts = o_casts['items']
#         for o_cast in o_casts:
#             o_cast['pg_rating'] = '+16'
#             o_cast['generic_title'] = "Хорошая трансляция"
#             o_cast['description'] = """В программе “Пусть говорят”  - самые яркие откровения звезд минувшего  телесезона.ПродюсерБари Алибасов в студии программы впервые узнал, что у него есть взрослая дочь. Новость о том, что
#                                        у него есть старший сын Павел, настигла и актера Александра Семчева.Алла Пугачева и Максим
#                                        Галкин объявили всей стране о том, что они стали родителями.Единственный сын легендарной
#                                        Клавдии Шульженко предоставил программе уникальное видео.Гостями студии были участники
#                                        самого запоминающего события года – Олимпиады в Сочи.Борис Моисеев, который долго восстанавливался после тяжелой болезни, пришел в студию в свой день рождения.Программе дал интервью Леонид Броневой, находящийся  в киевской больнице.Певица Екатерина Шаврина выговорилась  после рокового ДТП, в котором погибла ее любимая сестра Татьяна.Нани Брегвадзе рассказала , как пела песню "Снегопад" для мамы одного из российских олигархов."""
#             o_cast['locations'] = [
#                 #{'id': "1", 'type': 'playfamily', 'quality': "", 'price': 0, 'price_type': 0, 'value': "/casts/0"},
#                 {'id': "2", 'type': 'ivi','quality': "hd", 'price': 9000, 'price_type': 2, 'value': "/casts/0"},
#                 {'id': "3", 'type': 'olltv', 'quality': "fhd", 'price': 100500, 'price_type': 2, 'value': "/casts/2"}
#             ]
#
#     except Exception, e:
#         o_casts = []
#
#     return o_casts


