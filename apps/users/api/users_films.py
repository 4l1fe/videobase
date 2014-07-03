# coding: utf-8

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Films
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL, APP_USERFILM_SUBS_TRUE
from apps.films.api.serializers import vbFilm
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE

films_type = {
    'f': [APP_FILM_FULL_FILM],
    's': [APP_FILM_SERIAL],
    'all': [APP_FILM_SERIAL, APP_FILM_FULL_FILM],
}


class UsersFilmsView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        page = request.QUERY_PARAMS.get('page', APP_USERS_API_DEFAULT_PAGE)
        per_page = request.QUERY_PARAMS.get('per_page', APP_USERS_API_DEFAULT_PER_PAGE)
        type_ = request.QUERY_PARAMS.get('type', 'all')
        try:
            ftype = films_type[type_]
        except KeyError as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        films = Films.objects.filter(uf_films_rel__user=user, type__in=ftype,
                                     uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)
        try:
            page = Paginator(films, per_page).page(page)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbFilm(page.object_list, request=self.request, many=True)

        result = {
            'per_page': page.paginator.per_page,
            'page': page.number,
            'total_cnt': page.paginator.count,
            'items': serializer.data,
        }

        return Response(result, status=status.HTTP_200_OK)

