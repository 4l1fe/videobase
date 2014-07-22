# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Genres
from apps.films.api.serializers import vbUserGenre


class UsersGenresView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        genres = Genres.get_all_genres(get_values=False).filter(genres__uf_films_rel__user=user).distinct()
        genres = set(i.get_root() for i in genres)

        serializer = vbUserGenre(genres, user=user, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
