# coding: utf-8

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films, FilmExtras
from apps.films.api.serializers import vbComment


#############################################################################################################
class ActNotwatchFilmView(APIView):
    """
    Returns to the movie comments
    """

    def __get_result(self, film_id, type):
        pass


    def get(self, request, film_id, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


    def delete(self, request, film_id, format=None, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)
