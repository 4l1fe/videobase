# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films, FilmExtras
from apps.films.api.serializers import vbExtra


#############################################################################################################
class ExtrasFilmView(APIView):
    """
    Returns extra information about movie
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


    def post(self, request, film_id, format=None, *args, **kwargs):
        # Выбираем и проверяем, что фильм существует
        o_film = self.__get_object(film_id)
        if type(o_film) == Response:
            return o_film

        # Init data
        type = request.DATA.get('type', False)
        filter = {
            'film': o_film.pk,
        }

        if type:
            filter.update({'type': type})

        o_extras = FilmExtras.objects.filter(**filter)
        serializer = vbExtra(o_extras, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
