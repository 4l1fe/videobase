# coding: utf-8

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films

from vb_film import vbFilmSerializer


#############################################################################################################
#
class DetailFilmView(APIView):
    """
    Detailed information about film
    """

    serializer_class = vbFilmSerializer

    def __get_object(self, pk):
        try:
            return Films.objects.get(pk=pk)
        except Exception as e:
            raise Http404


    def __get_result(self, film_id, **kwargs):
        film = self.__get_object(film_id)
        serializer = vbFilmSerializer(film, extend=True)

        return serializer


    def post(self, request, film_id, format=None, *args, **kwargs):
        serializer = self.__get_result(film_id)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, film_id, format=None, *args, **kwargs):
        serializer = self.__get_result(film_id)

        return Response(serializer.data, status=status.HTTP_200_OK)
