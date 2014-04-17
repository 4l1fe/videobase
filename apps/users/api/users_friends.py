# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class UsersFriendsView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, user_id, *args, **kwargs):
        pass
