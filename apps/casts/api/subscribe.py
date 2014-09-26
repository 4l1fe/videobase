# coding: utf-8

from datetime import timedelta

from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.casts.tasks import cast_notification
from apps.casts.models import Casts, UsersCasts
from apps.casts.constants import APP_CASTS_START_NOTIFY



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

            # Проверка, что еще не подписан
            if user_cast.subscribed is None:
                user_cast.subscribed = timezone.now()
                user_cast.save()

                # Отправка email о трансляции
                delta_notify = cast.start - timedelta(minutes=APP_CASTS_START_NOTIFY)
                if user_cast.subscribed <= delta_notify:
                    cast_notification.apply_async(
                        kwargs={
                            'cast': cast.id,
                            'user': request.user.id
                        },
                        eta=delta_notify,
                        expires=cast.start
                    )

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
