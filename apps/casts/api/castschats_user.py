# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.casts.models import CastsChatsUsers
from apps.users.api.serializers import vbUser
from apps.casts.constants import CCU_ONLINE
from videobase.settings import DEFAULT_REST_API_RESPONSE



class CastsChatsUsersView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, castchat_id, *args, **kwargs):
        try:
            users = [ccu.user for ccu in CastsChatsUsers.objects.filter(cast_id=castchat_id, status=CCU_ONLINE)]

            return Response(vbUser(users, many=True).data, status=status.HTTP_200_OK)

        except CastsChatsUsers.DoesNotExist:
            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_404_NOT_FOUND)
