# coding: utf-8

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films

from vb_film import vbFilmSerializer


#############################################################################################################
#
class SimilarFilmView(APIView):
    """
    Return similar information by film
    """

    def __get_result(self, film_id):
        try:
            result = Films.objects.prefetch_related('persons').get(pk=film_id)
        except Films.DoesNotExist:
            raise Http404

        return result.persons.all()


    def get(self, request, film_id, format=None, *args, **kwargs):
        result = self.__get_result(film_id)
        serializer = vbFilmSerializer(result, extend=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
