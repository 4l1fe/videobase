# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import Feed
from apps.films.models import UsersFilms, UsersPersons
from apps.users.api.serializers import vbFeedElement


class UsersFeedsView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        pass
