# coding: utf-8

from datetime import date

from django.db.models import Q
from django.core.cache import cache
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.api.serializers import vbFilm
from apps.films.models import Films
from apps.films.forms import SearchForm
from apps.contents.models import Contents, Locations

import videobase.settings as settings
import sys

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
        film_group = 0
        location_group = 0

        for i in ['text', 'year_old', 'genre', 'rating', 'per_page', 'page']:
            if i in data.data:
                film_group += 1
                break

        if 'price' in data.data:
            location_group += 1

        return data.cleaned_data, film_group, location_group


    def search_by_films(self, filter):
        o_search = Films.objects.extra(
                where=['EXTRACT(year FROM "films"."release_date") <= %s'],
                params=[date.today().year],
            )

        # Поиск по имени
        if filter.get('text'):
            o_search = o_search.filter(Q(name__icontains=filter['text']) | Q(name_orig__icontains=filter['text']))

        # Поиск по количеству прошедших лет
        if filter.get('year_old'):
            o_search = o_search.extra(
                where=['EXTRACT(year FROM AGE(current_date, "films"."release_date")) < %s'],
                params=[filter['year_old']],
            )

        # Поиск по рейтингу
        if filter.get('rating'):
            o_search = o_search.filter(rating_cons__gte=filter['rating'])

        # Поиск по жанрам
        if filter.get('genre'):
            o_search = o_search.filter(genres=filter['genre'])

        return o_search


    def search_by_location(self, filter, o_search=None):
        o_loc = Locations.objects.all()

        if not o_search is None:
            list_film_pk = set(o_search.values_list('id', flat=True))
            conts_dict = dict(Contents.objects.filter(film__in=list_film_pk).values_list('id', 'film'))
            o_loc = o_loc.filter(content__in=conts_dict.keys())

        o_loc = o_loc.distinct('content').values_list('content', flat=True)

        if filter.get('price'):
            o_loc = o_loc.filter(price__lte=filter['price'])

        # Пересечение
        if o_search is None:
            list_films_by_content = Contents.objects.filter(pk__in=o_loc).\
                values_list('film', flat=True).distinct('film')
        else:
            list_films_by_content = list_film_pk & set([conts_dict[i] for i in o_loc if i in conts_dict])

        return list_films_by_content

    def use_cache(self):
        if 'test' in sys.argv:
            return False
        else:
            auth = self.request.user and self.request.user.is_authenticated()
            if auth:
                return False

            return not settings.DEBUG


    def get(self, request, format=None, *args, **kwargs):
        # Copy post request
        self.get_copy = request.GET.copy()

        form = SearchForm(data=self.get_copy)
        if form.is_valid():
            # Init data
            filter, film_group, location_group = self.parse_post(form)
            cache_key = u'{0}({1})'.format(self.__class__.__name__,
                                          ':'.join([i if isinstance(i, basestring) else str(i) for i in filter.values()]))
            result = cache.get(cache_key) if self.use_cache() else None

            if result is None:
                o_search = self.search_by_films(filter)

                list_films_by_content = []
                if location_group > 0:
                    list_films_by_content = self.search_by_location(filter, o_search)
                else:
                    if filter.get('instock'):
                        list_films_by_content = self.search_by_location(filter, o_search)

                # Пересечение не пусто
                if len(list_films_by_content):
                    o_search = Films.objects.filter(pk__in=list_films_by_content)
                else:
                    if filter.get('instock'):
                        list_films_by_content = self.search_by_location(filter, o_search)

                        if len(list_films_by_content):
                            o_search = Films.objects.filter(pk__in=list_films_by_content)

                try:
                    page = Paginator(o_search.order_by('-rating_sort'), per_page=filter['per_page']).page(filter['page'])
                except Exception as e:
                    return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

                serializer = vbFilm(page.object_list, request=self.request, many=True)

                result = {
                    'total_cnt': page.paginator.count,
                    'per_page': page.paginator.per_page,
                    'page': page.number,
                    'items': serializer.data,
                }

                if self.use_cache():
                    try:
                        cache.set(cache_key, result, 300)
                    except:
                        pass

            return Response(result, status=status.HTTP_200_OK)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
