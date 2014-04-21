# coding: utf-8

from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.films.models import Films, UsersFilms
from apps.films.constants import APP_USERFILM_STATUS_NOT_WATCH, APP_USERFILM_STATUS_UNDEF


#############################################################################################################
class ActNotwatchFilmView(APIView):
    """
    Method get:
        - Sets subscribe to the movie

    Method delete:
        - Delete subscribe to the movie
    """

    permission_classes = (IsAuthenticated,)

    def __get_object(self, film_id):
        """
        Return object Films or Response object with 404 error
        """
        try:
            result = Films.objects.get(pk=film_id)
        except Films.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result


    def get(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        not_watch = APP_USERFILM_STATUS_NOT_WATCH
        filter = {
            'user': request.user,
            'film': o_film,
        }

        # Устанавливаем подписку
        with transaction.atomic():
            try:
                o_subs = UsersFilms(status=not_watch, **filter)
                o_subs.save()
            except Exception as e:
                try:
                    UsersFilms.objects.filter(**filter).update(status=not_watch)
                except Exception as e:
                    return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }

        # Удалим подписку
        UsersFilms.objects.filter(**filter).update(status=APP_USERFILM_STATUS_UNDEF)

        return Response(status=status.HTTP_200_OK)
