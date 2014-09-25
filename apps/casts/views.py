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
            o_cast['generic_title'] = "Хорошая трансляция"
            o_cast['description'] = """В программе “Пусть говорят”  - самые яркие откровения звезд минувшего  телесезона.ПродюсерБари Алибасов в студии программы впервые узнал, что у него есть взрослая дочь. Новость о том, что
                                       у него есть старший сын Павел, настигла и актера Александра Семчева.Алла Пугачева и Максим
                                       Галкин объявили всей стране о том, что они стали родителями.Единственный сын легендарной
                                       Клавдии Шульженко предоставил программе уникальное видео.Гостями студии были участники
                                       самого запоминающего события года – Олимпиады в Сочи.Борис Моисеев, который долго восстанавливался после тяжелой болезни, пришел в студию в свой день рождения.Программе дал интервью Леонид Броневой, находящийся  в киевской больнице.Певица Екатерина Шаврина выговорилась  после рокового ДТП, в котором погибла ее любимая сестра Татьяна.Нани Брегвадзе рассказала , как пела песню "Снегопад" для мамы одного из российских олигархов."""
            o_cast['locations'] = [
                {'type': "", 'quality': "", 'price': 0, 'price_type': 0, 'value': "/casts/0"},
                {'type': "", 'quality': "hd", 'price': 9000, 'price_type': 0, 'value': "/casts/0"},
                {'type': "", 'quality': "fhd", 'price': 100500, 'price_type': 0, 'value': "/casts/2"}
            ]

    except Exception, e:
        o_casts = []

    return o_casts