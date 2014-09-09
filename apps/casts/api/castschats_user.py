# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.casts.models import CastsChatsUsers, Casts

from apps.users.api.serializers import vbUser


#############################################################################################################
class CastsChatsUsersView(APIView):
    """
    Cast info
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, castchat_id, *args, **kwargs):
        try:
            cast = Casts.objects.get(pk=1)
            users = [ccu.user for ccu in CastsChatsUsers.objects.get(cast=cast)]
            
            return Response(vbUser(users, many=True).data, status=status.HTTP_200_OK)

        except CastsChatsUsers.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
