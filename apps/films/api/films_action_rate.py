# coding: utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.films.forms import RatingForm
from apps.films.models import Films, UsersFilms
from apps.users import Feed

#############################################################################################################


class ActRateFilmView(APIView):
    """
    Method post:
        - Sets rating for a movie by user

    Method delete:
        - Sets rating as None for a movie by user
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

    def put(self, request, film_id, format=None, *args, **kwargs):
        form = RatingForm(request.DATA)
        if form.is_valid():
            # Выбираем и проверяем, что фильм существует
            o_film = self.__get_object(film_id)
            if isinstance(o_film, Response):
                return o_film

            # Init data
            rating = form.cleaned_data['rating']
            filter_ = {
                'user': request.user,
                'film': o_film,
            }

            obj_val = {
                'id': o_film.id,
                'name': o_film.name
            }

            obj_valr = {
                'id': o_film.id,
                'name': o_film.name,
                'rating': rating
            }

            # Устанавливаем оценку
            try:
                o_user_film = UsersFilms(rating=rating, **filter_)
                o_user_film.save()
                Feed.objects.create(user=request.user, type='film-r', object=obj_valr)
            except Exception as e:
                try:
                    UsersFilms.objects.filter(**filter_).update(rating=rating)
                    for f in Feed.objects.filter(user=request.user, type='film-r').iterator():   # До этого момента Feed
                        if all(item in f.object.items() for item in obj_val.items()): f.delete() # с типом film-nw может и не быть
                    Feed.objects.create(user=request.user, type='film-r', object=obj_valr)       # значит нечего обновлять
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK)

        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        filter_ = {'user': request.user.pk,
                  'film': o_film.pk}
        obj_val = {'id': o_film.id, 'name': o_film.name}

        # Удалим оценку
        UsersFilms.objects.filter(**filter_).update(rating=None)
        for f in Feed.objects.filter(user=request.user, type='film-r').iterator():
            if all(item in f.object.items() for item in obj_val.items()): f.delete()

        return Response(status=status.HTTP_200_OK)
