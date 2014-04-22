# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.films.api.serializers import vbPerson


#############################################################################################################
class PersonsFilmView(APIView):
    """
    Returns all persons by film
    """

    def __get_object(self, film_id):
        """
        Return object Films or Response object with 404 error
        """

        try:
            result = Films.objects.prefetch_related('persons').get(pk=film_id)
            result = result.persons.all()
        except Films.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result


    def get(self, request, film_id, format=None, *args, **kwargs):
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        serializer = vbPerson(o_film)

        return Response(serializer.data, status=status.HTTP_200_OK)
