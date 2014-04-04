# coding: utf-8

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films, FilmExtras

from vb_film import vbExtrasSerializer


#############################################################################################################
#
class ExtrasFilmView(APIView):
    """
    Return extras information by film
    """

    def __get_film_id(self, film_id):
        o_film = Films.objects.get(pk=film_id)
        return o_film.pk

    def __get_result(self, film_id, type):
        try:
            filter = {
                'film': self.__get_film_id(film_id),
            }

            if type:
                filter.update({'etype': type})

            o_extras = FilmExtras.objects.filter(**filter)
        except Films.DoesNotExist:
            raise Http404

        return o_extras


    def get(self, request, film_id, format=None, *args, **kwargs):
        type = None
        if request.DATA.get('type'):
            type = request.DATA['type']

        result = self.__get_result(film_id, type)
        serializer = vbExtrasSerializer(result)

        return Response(serializer.data, status=status.HTTP_200_OK)
