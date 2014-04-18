# coding: utf-8
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Films
from apps.films.constants import APP_FILM_FULL_FILM, APP_FILM_SERIAL, APP_USERFILM_STATUS_SUBS
from apps.films.api.serializers import vbFilm

films_type = {
    'f': [APP_FILM_FULL_FILM],
    's': [APP_FILM_SERIAL],
    'all': [APP_FILM_SERIAL, APP_FILM_FULL_FILM],
}


class UsersFilmsView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return Response({'e': e.message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        all_user_films = user.films.all()
        page = request.DATA.get('page', 1)
        per_page = request.DATA.get('per_page', 10)
        type = request.DATA.get('type', 'all')
        try:
            ftype = films_type[type]
        except KeyError as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        user_films_id = all_user_films.filter(film__type__in=ftype,
                                           status=APP_USERFILM_STATUS_SUBS).\
            values_list('film', flat=True)
        films = Films.objects.filter(pk__in=user_films_id)
        try:
            films_per_page = Paginator(films, per_page).page(page)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        total_cnt = all_user_films.count()
        serializer = vbFilm(films_per_page.object_list, many=True)

        result = {
            'per_page': per_page,
            'page': page,
            'total_cnt': total_cnt,
            'items': serializer.data,
        }

        return Response(result, status=status.HTTP_200_OK)

