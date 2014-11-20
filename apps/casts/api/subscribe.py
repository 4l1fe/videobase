# coding: utf-8

from datetime import timedelta

from django.utils import timezone

from kombu import Queue, Producer

from videobase.celery import app
from celery.utils import uuid
from videobase.settings import X_DEAD_EXCHANGE, MAIN_EXCHANGE, NOTIFY_QUEUE

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
            user_cast, create = UsersCasts.objects.get_or_create(user=request.user, cast=cast)

            # Проверка, что еще не подписан
            if user_cast.subscribed is None:
                user_cast.subscribed = timezone.now()
                user_cast.save()

                # Отправка email о трансляции
                delta_notify = cast.start - timedelta(minutes=APP_CASTS_START_NOTIFY)
                if user_cast.subscribed <= delta_notify:
                    # Расчет времени
                    expires = int((cast.start - user_cast.subscribed).total_seconds()) * 1000
                    expiration = int((delta_notify - user_cast.subscribed).total_seconds()) * 1000

                    with app.connection() as conn:
                        name_queue = 'cast_{id}'.format(id=cast_id)
                        cast_queue = app.amqp.queues[NOTIFY_QUEUE]
                        queue = Queue(
                            name=name_queue,
                            exchange=X_DEAD_EXCHANGE,
                            routing_key='wait.{name}'.format(name=name_queue),
                            queue_arguments={
                                'x-dead-letter-exchange'   : MAIN_EXCHANGE.name,
                                'x-dead-letter-routing-key': cast_queue.routing_key,
                                'x-expires'                : expires
                            }
                        )

                        channel = conn.channel()
                        producer = Producer(channel, exchange=X_DEAD_EXCHANGE)
                        producer.publish(
                            exchange=X_DEAD_EXCHANGE.name,
                            routing_key='wait.{name}'.format(name=name_queue),
                            declare=[cast_queue, queue],
                            body={
                                'kwargs': {'cast': cast.id, 'user': request.user.id},
                                'task': 'cast_notification', 'id': uuid()
                            },
                            **{
                                'expiration': str(expiration),
                                'delivery_mode': 2
                            }
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
