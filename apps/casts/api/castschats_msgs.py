# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.casts.models import CastsChatsMsgs
from apps.casts.forms import CastsChatGetForm
from apps.casts.api.serializers import vbCastChatMsg
from videobase.settings import DEFAULT_REST_API_RESPONSE


transform_map = {
    'id_low': lambda query, arg: query.filter(id__gte=arg),
    'id_high': lambda query, arg: query.filter(id__lte=arg),
    'limit': lambda query, arg: query[:arg]
}


class CastsChatsMsgsView(APIView):

    def get(self, request, cast_id, *args, **kwargs):
        try:
            data = request.GET.copy()
            form = CastsChatGetForm(data=data)
            if form.is_valid():
                query = CastsChatsMsgs.objects.filter(cast__id=cast_id)

                for field in form.cleaned_data:
                    if form.cleaned_data[field]:
                        query = transform_map[field](query, form.cleaned_data[field])

                return Response(vbCastChatMsg(query, many=True).data, status=status.HTTP_200_OK)

            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
