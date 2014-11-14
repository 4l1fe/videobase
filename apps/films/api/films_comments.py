# coding: utf-8

from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.contents.models import Comments, Contents
from apps.films.api.serializers import vbComment
from apps.films.constants import APP_COMMENTS_API_DEFAULT_PAGE, APP_COMMENTS_API_DEFAULT_PER_PAGE

from videobase.settings import DEFAULT_REST_API_RESPONSE


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
        except Contents.DoesNotExist:
            result = Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_404_NOT_FOUND)

        return result


    def __validation_pagination(self, page, per_page, filter):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = APP_COMMENTS_API_DEFAULT_PAGE

        if page < APP_COMMENTS_API_DEFAULT_PAGE:
            page = APP_COMMENTS_API_DEFAULT_PAGE

        try:
            per_page = int(per_page)
        except (TypeError, ValueError):
            per_page = APP_COMMENTS_API_DEFAULT_PER_PAGE

        if 0 < per_page > APP_COMMENTS_API_DEFAULT_PER_PAGE:
            per_page = APP_COMMENTS_API_DEFAULT_PER_PAGE

        filter.update({'per_page': per_page, 'page': page})
        return filter

    def get(self, request, film_id, format=None, *args, **kwargs):
        content = self.__get_object(film_id)
        if type(content) == Response:
            return content

        # Копируем запрос, т.к. в форме его изменяем
        copy_req = request.GET.copy()

        # Проверка пагинации
        filter = self.__validation_pagination(copy_req.get('page'), copy_req.get('per_page'), {})

        o_comments = Comments.objects.filter(content=content).order_by('-created')

        try:
            page = Paginator(o_comments, per_page=filter['per_page']).page(filter['page'])

            result = {
                'total_cnt': page.paginator.count,
                'ipp': page.paginator.per_page,
                'page': page.number,
                'items': vbComment(page.object_list, many=True).data,
            }

        except Exception as e:
            return Response({
                'total_cnt': len(o_comments),
                'ipp': len(o_comments),
                'page': filter['page'],
                'items': [],
            }, status=status.HTTP_200_OK)

        return Response(result, status=status.HTTP_200_OK)
