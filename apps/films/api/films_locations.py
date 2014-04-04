# coding: utf-8

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.contents.models import Contents, Locations

from vb_locations import vbLocationsFilmSerializer


#############################################################################################################
#
class LocationsFilmView(APIView):
    """
    All locations by film
    """

    def __get_obj_content(self, film_id):
        try:
            content = Contents.objects.get(film=film_id)
            return content.id
        except Contents.DoesNotExist:
            raise Http404


    def __get_all_locations(self, content_id):
        location = Locations.objects.filter(content=content_id).defer('content')
        return location


    def get(self, request, film_id, format=None, *args, **kwargs):
        content = self.__get_obj_content(film_id)
        location = self.__get_all_locations(content)
        serializer = vbLocationsFilmSerializer(location)

        return Response({'test': 'test'}, status=status.HTTP_200_OK)
