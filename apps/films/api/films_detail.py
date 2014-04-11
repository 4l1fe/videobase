# coding: utf-8

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.films.api.serializers import vbFilm


#############################################################################################################
class DetailFilmView(APIView):
    """
    Return detailed information about movie
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


    def __get_result(self, film_id, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            raise Http404

        serializer = vbFilm(o_film, extend=True, persons=True)

        return serializer


    def post(self, request, film_id, format=None, *args, **kwargs):
        serializer = self.__get_result(film_id)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, film_id, format=None, *args, **kwargs):
        serializer = self.__get_result(film_id)

        return Response(serializer.data, status=status.HTTP_200_OK)
