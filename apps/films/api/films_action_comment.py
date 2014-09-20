# coding: utf-8
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.contents.models import Comments, Contents
from apps.films.forms import CommentForm
from apps.films.models import Films
from apps.users import Feed
from apps.users.constants import FILM_COMMENT

from videobase.settings import DEFAULT_REST_API_RESPONSE

from cgi import escape
import re
#############################################################################################################


class ActCommentFilmView(APIView):
    """
    Method post:
        - Makes insert a comment to the movie
    """

    permission_classes = (IsAuthenticated,)

    def __get_object(self, film_id):
        """
        Return object Contents or Response object with 404 error
        """

        try:
            o_film = Films.objects.get(id=film_id)
        except ObjectDoesNotExist:
            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_404_NOT_FOUND)

        try:
            o_content = Contents.objects.get(film=o_film.id)
        except Exception, e:
            try:
                o_content = Contents(
                    film=o_film, name=o_film.name, name_orig=o_film.name_orig,
                    description=o_film.description, release_date=o_film.release_date,
                    viewer_cnt=0, viewer_lastweek_cnt=0, viewer_lastmonth_cnt=0
                )
                o_content.save()
            except Exception, e:
                return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_404_NOT_FOUND)

        return o_content

    def post(self, request, film_id, format=None, *args, **kwargs):
        form = CommentForm(request.DATA)
        if form.is_valid():
            # Выбираем и проверяем, что фильм существует
            o_content = self.__get_object(film_id)
            if isinstance(o_content, Response):
                return o_content

            # Init data
            filter_ = {
                'user': request.user,
                'text': re.sub('\n+', '<br>', escape(form.cleaned_data['text'])),
                'content': o_content
            }

            o_com = Comments.objects.create(**filter_)
            Feed.objects.create(user=request.user, type=FILM_COMMENT, obj_id=o_com.id, child_obj_id=o_content.film_id)

            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_200_OK)

        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, film_id, format=None, *args, **kwargs):
        return self.post(request, film_id, format=None, *args, **kwargs)

