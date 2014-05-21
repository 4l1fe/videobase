# coding: utf-8
import json
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.contents.models import Comments, Contents
from apps.films.forms import CommentForm
from apps.films.models import Films
from apps.users import Feed


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
            f = Films.objects.get(id=film_id)
            c, created = Contents.objects.get_or_create(film=f, name=f.name, name_orig=f.name_orig,
                                                    description=f.description, release_date=f.release_date,
                                                    viewer_cnt=0, viewer_lastweek_cnt=0, viewer_lastmonth_cnt=0)

            return c
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, film_id, format=None, *args, **kwargs):
        form = CommentForm(request.DATA)
        print(request.DATA)
        if form.is_valid():
            # Выбираем и проверяем, что фильм существует
            o_content = self.__get_object(film_id)
            if isinstance(o_content, Response):
                return o_content

            # Init data
            filter = {'user': request.user,
                      'text': form.cleaned_data['text'],
                      'content': o_content}

            o_com = Comments.objects.create(**filter)
            obj_val = json.dumps({'id': o_com.id, 'text': o_com.text,
                                  'film': {'id': o_content.film_id, 'name': o_content.name}})
            Feed.objects.create(user=request.user, type='film-c', object=obj_val)  # под каждый комент новое событие.
            return Response(status=status.HTTP_200_OK)

        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)