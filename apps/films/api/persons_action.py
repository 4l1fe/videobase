# coding: utf-8

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users import Feed
from apps.users.constants import PERSON_SUBSCRIBE
from apps.films.models import UsersPersons, Persons
from videobase.settings import DEFAULT_REST_API_RESPONSE


class PersonActionAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def _handle(self, subscribed, request, format=None, resource_id=None):
        try:
            person = Persons.objects.get(id=resource_id)
            filter_ = {
                'user': request.user,
                'person': person
            }
            up, up_created = UsersPersons.objects.get_or_create(**filter_)
            up.subscribed = subscribed
            up.save()

            if subscribed:
                feed, created = Feed.objects.get_or_create(user=self.request.user, type=PERSON_SUBSCRIBE, obj_id=person.id)
                if not created:
                    feed.save()
            else:
                Feed.objects.filter(user=request.user, type=PERSON_SUBSCRIBE, obj_id=person.id).delete()

            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_200_OK)

        except Exception, e:
            return Response(DEFAULT_REST_API_RESPONSE, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None, resource_id=None):
        return self._handle(1, request, format, resource_id)


    def delete(self, request, format=None, resource_id=None):
        return self._handle(0, request, format, resource_id)
