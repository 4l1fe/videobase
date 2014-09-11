# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.casts.models import Casts
from apps.casts.api.serializers import vbCast


#############################################################################################################
class CastsExtrasView(APIView):
    """
    Cast info
    """

    def get(self, request, cast_id, *args, **kwargs):
        try:
            
            return Response(vbExtra(cast).data, status=status.HTTP_200_OK)
        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
            

