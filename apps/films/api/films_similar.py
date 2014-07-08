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


    def logic_calcultate(self, o_film, data_flag=False):
        o_similar = Films.similar_api(o_film)
        serializer = vbFilm(o_similar, request=self.request, many=True).data

        return Response(serializer, status=status.HTTP_200_OK) if not data_flag else serializer


    def get(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_result(film_id)
        if type(o_film) == Response:
            return o_film

        return self.logic_calcultate(o_film)
