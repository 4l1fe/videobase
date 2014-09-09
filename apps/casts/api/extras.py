# coding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.casts.models import Casts, CastsExtras
from apps.films.api.serializers import vbExtra


#############################################################################################################
class CastsExtraView(APIView):
    """
    Cast info
    """

    def get(self, request, cast_id, *args, **kwargs):
        try:
            cast_extras = CastsExtras.objects.filter(cast__id=cast_id)
            return Response(vbExtra([ce.extra for ce in cast_extras],many=True).data, status=status.HTTP_200_OK)
        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
            