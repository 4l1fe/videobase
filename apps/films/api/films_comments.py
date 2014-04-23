# coding: utf-8

from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.contents.models import Comments, Contents
from apps.films.api.serializers import vbComment


#############################################################################################################
class CommentsFilmView(APIView):
    """
    Returns to the movie comments
    """

    def __get_object(self, film_id):
        """
        Return object Films or Response object with 404 error
        """

        try:
            result = Contents.objects.get(film=film_id)
        except Films.DoesNotExist:
            result = Response(status=status.HTTP_404_NOT_FOUND)

        return result


    def post(self, request, film_id, format=None, *args, **kwargs):
        content = self.__get_object(film_id)
        if type(content) == Response:
            return content

        # Init data
        page = request.DATA.get('page', 1)
        per_page = request.DATA.get('per_page', 10)

        filter = {
            'content': content.film.pk,
        }

        o_comments = Comments.objects.filter(**filter)

        try:
            page = Paginator(o_comments, per_page=per_page).page(page)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbComment(page.object_list, many=True)
        result = {
            'total_cnt': page.paginator.count,
            'per_page': page.paginator.per_page,
            'page': page.number,
            'items': serializer.data,
        }

        return Response(result, status=status.HTTP_200_OK)
