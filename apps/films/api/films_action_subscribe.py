# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.films.models import Films, UsersFilms
from apps.films.constants import APP_USERFILM_SUBS_TRUE, APP_USERFILM_SUBS_FALSE, APP_FILM_SERIAL


#############################################################################################################
class ActSubscribeFilmView(APIView):
    """
    Method get:
        - Sets subscribe for a serial by user

    Method delete:
        - Delete subscribe for a serial by user
    """

    permission_classes = (IsAuthenticated,)

    def __get_object(self, film_id):
        """
        Return object Films or Response object with 404 error
        """
        try:
            result = Films.objects.get(pk=film_id, )
        except Films.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result


    def get(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Проверка, что это сериал
        if o_film.type != APP_FILM_SERIAL:
            return Response({'error': u'Нельзя подписаться на фильм'}, status=status.HTTP_400_BAD_REQUEST)

        # Init data
        subscribed = APP_USERFILM_SUBS_TRUE
        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }

        # Устанавливаем подписку
        try:
            o_subs = UsersFilms(subscribed=subscribed, **filter)
            o_subs.save()
        except Exception as e:
            try:
                UsersFilms.objects.filter(**filter).update(subscribed=subscribed)
            except Exception as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Проверка, что это сериал
        if o_film.type != APP_FILM_SERIAL:
            return Response({'error': u'Нельзя отписаться от фильма'}, status=status.HTTP_400_BAD_REQUEST)

        # Init data
        subscribed = APP_USERFILM_SUBS_FALSE
        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }

        # Удалим подписку
        UsersFilms.objects.filter(**filter).update(subscribed=subscribed)

        return Response(status=status.HTTP_200_OK)
