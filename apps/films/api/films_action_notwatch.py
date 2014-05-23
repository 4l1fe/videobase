# coding: utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.films.models import Films, UsersFilms
from apps.films.constants import APP_USERFILM_STATUS_NOT_WATCH, APP_USERFILM_STATUS_UNDEF
from apps.users import Feed


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
            return Films.objects.get(pk=film_id)
        except Films.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_object(film_id)
        if isinstance(o_film, Response):
            return o_film

        # Init data
        not_watch = APP_USERFILM_STATUS_NOT_WATCH
        filter_ = {'user': request.user,
                  'film': o_film}
        obj_val = {'id': o_film.id, 'name': o_film.name}

        # Устанавливаем подписку
        try:
            o_subs = UsersFilms(status=not_watch, **filter_)
            o_subs.save()
            Feed.objects.create(user=request.user, type='film-nw', object=obj_val)
        except Exception as e:
            try:
                UsersFilms.objects.filter(**filter_).update(status=not_watch)
            except Exception as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


        return Response(status=status.HTTP_200_OK)

    def put(self, request, film_id, format=None, *args, **kwargs):
        return self.get(request, film_id, format=None, *args, **kwargs)

    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        filter = {'user': request.user.pk,
                  'film': o_film.pk}
        obj_val = {'id': o_film.id, 'name': o_film.name}
        # Удалим подписку
        UsersFilms.objects.filter(**filter).update(status=APP_USERFILM_STATUS_UNDEF)
        Feed.objects.filter(user=request.user, type='film-nw', object=obj_val).delete()

        return Response(status=status.HTTP_200_OK)