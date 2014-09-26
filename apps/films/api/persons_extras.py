# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.api.serializers import vbExtra
from apps.films.models import Persons, PersonsExtras


class PersonsExtrasAPIView(APIView):
    """

    """

    def get(self, request, format=None, resource_id=None, extend=False, type=None):
        try:
            filter = {
                'person': Persons.objects.get(id=resource_id)
            }

            if not type is None:
                filter.update({'type': type})

            pes = PersonsExtras.objects.filter(**filter)
            result = vbExtra(instance=pes, many=True).data
            return Response(result, status=status.HTTP_200_OK)

        except Exception, e:
            return Response(status=status.HTTP_404_NOT_FOUND)
