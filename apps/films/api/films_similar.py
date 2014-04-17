# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.films.api.serializers.vb_film import vbFilm


#############################################################################################################
class SimilarFilmView(APIView):
    """
    Returns the same movies on film
    """

    def __get_result(self, film_id):
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
        o_film = self.__get_result(film_id)
        if type(o_film) == Response:
            return o_film

        # Логика для выборки похожих фильмов
        list_genres = [i.pk for i in o_film.genres.all()]

        o_similar = Films.objects.filter(genres__in=list_genres).order_by('-rating_cons')[:10]

        serializer = vbFilm(o_similar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
