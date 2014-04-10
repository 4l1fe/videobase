# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.forms import RatingForm
from apps.films.models import Films, UsersFilms


#############################################################################################################
class ActRateFilmView(APIView):
    """
    """

    def __get_object_film(self, film_id):
        """
        Return object Films or Response object with 404 error
        """
        try:
            result = Films.objects.get(pk=film_id)
        except Films.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result

    def post(self, request, film_id, format=None, *args, **kwargs):
        form = RatingForm(request.DATA)
        if form.is_valid():
            # Выбираем и проверяем, что фильм существует
            o_film = self.__get_object_film(film_id)
            if type(o_film) == Response:
                return o_film

            # Init data
            rating = form.cleaned_data['rating']
            filter = {
                'user': request.user.pk,
                'film': o_film.pk,
            }

            # Устанавливаем оценку
            try:
                o_user_film = UsersFilms(rating=rating, **filter)
                o_user_film.save()
            except Exception as e:
                try:
                    UsersFilms(**filter).update(rating=rating)
                except Exception as e:
                    return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK)
        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object_film(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        filter = {
            'user': request.user.pk,
            'film': o_film.pk,
        }

        # Удалим оценку
        UsersFilms.objects.filter(**filter).update(rating=None)

        return Response(status=status.HTTP_200_OK)
