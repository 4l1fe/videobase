# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.casts.models import Casts, UsersCasts

from django.utils import timezone


################################################################################
class CastsSubscribeView(APIView):
    """
    Cast info
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, cast_id, *args, **kwargs):
        try:
            cast = Casts.objects.get(pk=cast_id)
            user_cast = UsersCasts.objects.get_or_create(user__id=request.user.id, cast=cast)
            return Response({'subscribed': bool(user_cast.subscribed)}, status=status.HTTP_200_OK)

        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, cast_id, *args, **kwargs):
        try:
            cast = Casts.objects.get(pk=cast_id)
            user_cast = UsersCasts.objects.get_or_create(user__id=request.user.id, cast=cast)
            user_cast.subscribed = timezone.now()
            user_cast.save()
            return Response({'subscribed': bool(user_cast.subscribed)}, status=status.HTTP_200_OK)

        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, cast_id, *args, **kwargs):
        try:
            cast = Casts.objects.get(pk=cast_id)
            user_cast = UsersCasts.objects.get(user__id=request.user.id, cast=cast)
            user_cast.subscribed = None
            
            return Response({}, status=status.HTTP_200_OK)

        except Casts.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        except UsersCasts.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)
