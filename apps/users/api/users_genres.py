# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Genres
from apps.films.api.serializers import vbUserGenre


class UsersGenresView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return Response({'e': e.message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        genres = Genres.objects.filter(genres__users_films__user=user)

        serializer = vbUserGenre(genres, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)