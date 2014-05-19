# coding: utf-8
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import UsersPersons, Persons


class PersonActionAPIView(APIView):
    '''

    '''

    def __users_person_set(self, user, person, subscribed):
        filter = {
            'user': user,
            'person': person,
        }

        try:
            up = UsersPersons.objects.get(**filter)
            up.subscribed = subscribed
        except UsersPersons.DoesNotExist, ue:
            up = UsersPersons(subscribed=subscribed, upstatus=0, **filter)
        finally:
            up.save()

    def _response_template(self, subscribed, request, format=None, resource_id=None):
        '''
        Template for responses
        '''

        try:
            person = Persons.objects.get(id=resource_id)
            self.__users_person_set(request.user, person, subscribed)
            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None, resource_id=None):
        return self._response_template(1, request, format, resource_id)

    def delete(self, request, format=None, resource_id=None):
        return self._response_template(0, request, format, resource_id)