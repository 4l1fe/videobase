# coding: utf-8

from django.http import Http404
from django.core.paginator import Paginator, InvalidPage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.api.serializers import vbFilm
from apps.films.models import Films
from apps.films.forms import SearchForm


#############################################################################################################
class SearchFilmsView(APIView):
    """
    Поиск по фильмам:
        text - Текст для поиска
        genre - id жанра
        year_old - Количество лет, прошедших с года выпуска
        rating - Рейтинг не меньше
        price - Стоимость не больше
        per_page - Количество фильмов на страницу
        page - Номер страницы
        instock - Фильм в наличии в кинотеатрах
    """

    def parse_post(self, data):
        filter = {}
        if data.get('text'):
            filter.update({'name': data['text']})

        if data.get('genre'):
            filter.update({'genre': data['genre']})

        if data.get('rating'):
            filter.update({'rating': data['rating']})

        if data.get('price'):
            filter.update({'price': data['price']})

        if data.get('instock'):
            filter.update({'instock': data['instock']})

        return filter


    def get(self, request, format=None, *args, **kwargs):
        # Init data
        page = request.QUERY_PARAMS.get('page', 1)
        per_page = request.QUERY_PARAMS.get('per_page', 12)

        filter = self.parse_post(request.QUERY_PARAMS)

        o_search = Films.objects.all()
        if filter.get('name'):
            o_search = o_search.filter(name__icontains=filter['name'])

        try:
            page = Paginator(o_search, per_page=per_page).page(page)
        except InvalidPage as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbFilm(page.object_list)

        result = {
            'total_cnt': page.paginator.num_pages,
            'per_page': page.paginator.per_page,
            'page': page.number,
            'items': serializer.data,
        }

        return Response(result, status=status.HTTP_200_OK)
