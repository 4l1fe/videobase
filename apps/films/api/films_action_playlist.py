# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films, UsersFilms
from apps.films.constants import APP_USERFILM_STATUS_SUBS, APP_USERFILM_SUBS_TRUE, APP_FILM_SERIAL


#############################################################################################################
class ActPlaylistFilmView(APIView):
    """
    Method get:
        - Sets subscribe to the serial

    Method delete:
        - Delete subscribe to the serial
    """

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
        add_params = {
            'status': APP_USERFILM_STATUS_SUBS,
        }

        # Если сериал
        if o_film.type != APP_FILM_SERIAL:
            add_params.update({'subscribe': APP_USERFILM_SUBS_TRUE})

        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }

        # Устанавливаем в плейлист
        try:
            o_subs = UsersFilms.object.get(**filter)
            return Response({'error': 'Уже подписан'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            try:
                o_subs = UsersFilms(**filter(add_params))
                o_subs.save()
            except Exception as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def delete(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Удаляем из плейлиста
        UsersFilms.objects.filter(pk=o_film.pk).delete()

        return Response(status=status.HTTP_200_OK)
