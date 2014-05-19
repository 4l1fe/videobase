# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import Persons
from apps.films.api.serializers import vbPerson


class PersonAPIView(APIView):

    def get(self, request, format=None, resource_id=None):
        try:
            p = Persons.objects.get(pk=resource_id)
            data = vbPerson(p).data
            u = request.user
            if u and u.is_authenticated():
                data = vbPerson(p, user=u).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None, resource_id=None):
        extend = request.DATA.get('extend', '')
        if extend.lower() == 'true':
            extend = True
        else:
            extend = False

        try:
            p = Persons.objects.get(pk=resource_id)
            data = vbPerson(p, extend=extend).data
            u = request.user
            if u and u.is_authenticated():
                data = vbPerson(p, extend=True, user=u).data
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)