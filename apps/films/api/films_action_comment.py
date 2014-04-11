# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.films.models import Films
from apps.contents.models import Comments, Contents
from apps.films.forms import CommentForm


#############################################################################################################
class ActCommentFilmView(APIView):
    """
    Method post:
        - Makes insert a comment to the movie
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


    def post(self, request, film_id, format=None, *args, **kwargs):
        form = CommentForm(request.DATA)
        if form.is_valid():
            # Выбираем и проверяем, что фильм существует
            o_content = self.__get_object(film_id)
            if type(o_content) == Response:
                return o_content

            # Init data
            filter = {
                'user': request.user.pk,
                'text': form.cleaned_data['text'],
                'content': o_content.pk,
            }

            try:
                o_com = Comments(**filter)
                o_com.save()
            except Exception as e:
                return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
