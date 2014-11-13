# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.casts.forms import CastChatSendForm
from apps.casts.models import Casts, CastsChats, CastsChatsMsgs
from videobase.settings import DEFAULT_REST_API_RESPONSE


class CastsChatSendView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, cast_id, format=None, *args, **kwargs):
        form = CastChatSendForm(request.DATA)
        if form.is_valid():
            try:
                cast = Casts.objects.get(pk=cast_id)
                
                cast_chat = CastsChats.objects.get_or_create(cast=cast, status=1)

                ccm = CastsChatsMsgs(cast=cast, user=request.user, text=form.cleaned_data['text'])
                ccm.save()

            except Casts.DoesNotExist:
                return Response({'error': 'There is no such cast with id {}'.format(cast_id)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_200_OK)

        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)
