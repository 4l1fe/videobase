# coding: utf-8
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.films.models import Films, UsersFilms
from apps.contents.models import Locations
from apps.films.constants import APP_USERFILM_SUBS_TRUE, APP_USERFILM_SUBS_FALSE, APP_FILM_SERIAL
from apps.users.models import Feed


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
            result = Locations.exist_location(film_id)
            if result:
                return Response({'error': u'Нельзя подписаться на фильм, потому что он уже появился в кинотеатрах'}, status=status.HTTP_400_BAD_REQUEST)

        # Init data
        subscribed = APP_USERFILM_SUBS_TRUE
        filter_ = {
            'user': request.user,
            'film': o_film,
        }
        obj_val = json.dumps(dict(id=o_film.id, name=o_film.name))

        # Устанавливаем подписку
        try:
            o_subs = UsersFilms(subscribed=subscribed, **filter_)
            o_subs.save()
            Feed.objects.create(user=request.user, type='film-s', object=obj_val)
        except Exception as e:
            try:
                UsersFilms.objects.filter(**filter_).update(subscribed=subscribed)
            except Exception as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Проверка, что это сериал
        if o_film.type != APP_FILM_SERIAL:
            result = Locations.exist_location(film_id)
            if result:
                return Response({'error': u'Нельзя отписаться от фильма'}, status=status.HTTP_400_BAD_REQUEST)

        # Init data
        subscribed = APP_USERFILM_SUBS_FALSE
        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }
        obj_val = json.dumps(dict(id=o_film.id, name=o_film.name))

        # Удалим подписку
        UsersFilms.objects.filter(**filter).update(subscribed=subscribed)
        try:
            Feed.objects.get(user=request.user, type='film-s', object=obj_val).delete()
        except Feed.DoesNotExist as e:  # если записи события вдруг нету, нет смысла что-либо делать.
            pass

        return Response(status=status.HTTP_200_OK)

    def put(self, request, film_id, format=None, *args, **kwargs):
        return self.get(request, film_id, format=format, *args, **kwargs)