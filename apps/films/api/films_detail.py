# coding: utf-8

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.films.forms import DetailForm
from apps.films.api.serializers import vbFilm

from videobase.settings import DEFAULT_REST_API_RESPONSE
#############################################################################################################
class DetailFilmView(APIView):
    """
    Return detailed information about movie
    """

    def __get_object(self, film_id, cleaned_data):
        """
        Return object Films or Response object with 404 error
        """

        prefetch = []
        if cleaned_data['extend']:
            prefetch.extend(['countries'])

        if cleaned_data['persons']:
            prefetch.append('persons')

        result = Films.objects.filter(pk=film_id).prefetch_related(*prefetch)
        if not len(result):
            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_404_NOT_FOUND)

        return result[0]


    def __get_result(self, film_id, cleaned_data, **kwargs):
        o_film = self.__get_object(film_id, cleaned_data)
        if type(o_film) == Response:
            raise Http404

        return vbFilm(o_film, request=self.request, **cleaned_data)


    def post(self, request, film_id, format=None, *args, **kwargs):
        form = DetailForm(data=request.POST)
        if form.is_valid():
            serializer = self.__get_result(film_id, form.cleaned_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(form.message, status=status.HTTP_200_OK)


    def get(self, request, film_id, format=None, *args, **kwargs):
        form = DetailForm(data=request.GET)
        if form.is_valid():
            serializer = self.__get_result(film_id, form.cleaned_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(form.message, status=status.HTTP_200_OK)
