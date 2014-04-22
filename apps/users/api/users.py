# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.users.api.serializers import vbUser


class UsersView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbUser(user, cer_usre=request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        ser_par = dict(extend=request.DATA.get('extend', False),
                       friends=request.DATA.get('friends', False),
                       genres=request.DATA.get('genres', False),
                       )

        serializer = vbUser(user, **ser_par)

        return Response(serializer.data, status=status.HTTP_200_OK)