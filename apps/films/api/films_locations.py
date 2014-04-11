# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.contents.models import Contents, Locations
from apps.films.api.serializers.vb_location import vbLocation


#############################################################################################################
class LocationsFilmView(APIView):
    """
    Returns all locations movie
    """

    def __get_object(self, film_id):
        """
        Return object Films or Response object with 404 error
        """

        try:
            result = Contents.objects.get(film=film_id)
        except Contents.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result


    def get(self, request, film_id, format=None, *args, **kwargs):
        o_content = self.__get_object(film_id)
        if type(o_content) == Response:
            return o_content

        o_location = Locations.objects.filter(content=o_content.pk).defer('content')
        serializer = vbLocation(o_location)

        return Response(serializer.data, status=status.HTTP_200_OK)
