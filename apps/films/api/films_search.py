# coding: utf-8

import sys
from datetime import date

from django.core.cache import cache
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.api.serializers import vbFilm
from apps.films.models import Films, Genres
from apps.films.forms import SearchForm
from apps.films.constants import APP_USERFILM_STATUS_NOT_WATCH, APP_FILMS_API_DEFAULT_PAGE, \
                                 APP_FILMS_API_DEFAULT_PER_PAGE
from apps.contents.models import Locations

import videobase.settings as settings

from utils.middlewares.local_thread import get_current_request

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

    def search_by_films(self, filter):
        o_search = Films.search_manager.filter(release_date__lte=date.today())\
            .order_by('-rating_sort')

            
        # Поиск по имени
        if filter.get('text'):
            o_search = o_search.search(filter['text'])

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
            o_search = o_search.distinct().filter(genres__in=Genres.get_children_list_id(filter['genre']))

        # Персонализация выборки
        if self.request.user.is_authenticated() and filter.get('recommend'):
            sql = """
            NOT "films"."id" IN (
                SELECT "users_films"."film_id" FROM "users_films"
                WHERE "users_films"."user_id" = %s AND
                      ("users_films"."status" = %s OR
                      "users_films"."rating" IS NOT NULL)
            )
            """

            o_search = o_search.extra(
                where=[sql],
                params=[self.request.user.pk, APP_USERFILM_STATUS_NOT_WATCH],
            )

        return o_search


    def search_by_location(self, filter, o_search=None):
        o_loc = Locations.objects.values_list('content__film', flat=True)

        if self.flag_price:
            o_loc = o_loc.filter(price__lte=filter['price'])

        if filter.get('instock'):
            o_loc = o_loc.distinct('content')

        return o_loc


    def use_cache(self):
        if 'test' in sys.argv:
            return False
        else:
            if self.request.user.is_authenticated():
                return False

            return not settings.DEBUG


    def validation_pagination(self, page, per_page, filter):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = APP_FILMS_API_DEFAULT_PAGE

        if page < APP_FILMS_API_DEFAULT_PAGE:
            page = APP_FILMS_API_DEFAULT_PAGE

        try:
            per_page = int(per_page)
        except (TypeError, ValueError):
            per_page = APP_FILMS_API_DEFAULT_PER_PAGE

        if 0 < per_page > APP_FILMS_API_DEFAULT_PER_PAGE:
            per_page = APP_FILMS_API_DEFAULT_PER_PAGE

        filter.update({'per_page': per_page, 'page': page})
        return filter


    def get(self, request, format=None, recommend=False, use_thread=False, *args, **kwargs):
        # Копируем запрос, т.к. в форме его изменяем
        self.get_copy = request.GET.copy()

        if recommend or self.get_copy.get('recommend'):
            self.get_copy['recommend'] = True

        if use_thread:
            self.request = get_current_request()

        # Валидируем форму
        form = SearchForm(data=self.get_copy)

        if form.is_valid():
            # Init data
            filter = self.validation_pagination(self.get_copy.get('page'), self.get_copy.get('per_page'), form.cleaned_data)

            self.flag_price = True if ('price' in filter and not filter['price'] is None) else False
            location_group = 1 if self.flag_price or filter.get('instock') else 0

            # Init cache params
            use_cache = self.use_cache()
            cache_key = u'{0}({1})'.format(
                self.__class__.__name__,
                ':'.join([i if isinstance(i, basestring) else str(i) for i in filter.values()])
            )

            # Проверим, есть ли результат в кеше
            result = cache.get(cache_key) if use_cache else None


            if result is None:
                # Наложение условий фильтрации на фильмы
                o_search = self.search_by_films(filter)

                if location_group > 0:
                    # Список фильмов удовлетворяющий условиям локации
                    list_films_by_content = self.search_by_location(filter, o_search)

                    # Наложение списка локации на выборку фильмов
                    o_search = o_search.filter(id__in=list_films_by_content)

                try:
                    page = Paginator(o_search, per_page=filter['per_page']).\
                        page(filter['page'])
                except Exception, e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Формируем ответ
                result = {
                    'total_cnt': page.paginator.count,
                    'per_page': page.paginator.per_page,
                    'page': page.number,
                    'items': vbFilm(page.object_list, request=self.request, many=True).data,
                }

                if use_cache:
                    try:
                        cache.set(cache_key, result, 300)
                    except Exception, e:
                        pass

            return Response(result, status=status.HTTP_200_OK)

        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
