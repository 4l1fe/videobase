# coding: utf-8
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import UsersPersons, Persons
from apps.users import Feed


class PersonActionAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def _update_or_create_feed(self, type_, obj_val):
        ffeeds = Feed.objects.filter(user=self.request.user, type=type_)
        feeds = [f for f in ffeeds]
        objs = [f.object for f in ffeeds]
        try:
            f = feeds[objs.index(obj_val)]
            f.save()
        except ValueError:
            Feed.objects.create(user=self.request.user, type=type_, object=obj_val)

    def _handle(self, subscribed, request, format=None, resource_id=None):
        try:
            person = Persons.objects.get(id=resource_id)
            filter_ = {'user': request.user,
                      'person': person}
            photo_url = person.photo.storage.url(person.photo.name)
            obj_val = {'id': person.id, 'name': person.name, 'photo': photo_url}

            up, up_created = UsersPersons.objects.get_or_create(**filter_)
            up.subscribed = subscribed
            up.save()
            self._update_or_create_feed('pers-s', obj_val)
            if not subscribed:
                for f in Feed.objects.filter(user=request.user, type='pers-s'):
                    if f.object == obj_val: f.delete()

            return Response(status=status.HTTP_200_OK)
        except Exception, e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None, resource_id=None):
        return self._handle(1, request, format, resource_id)

    def delete(self, request, format=None, resource_id=None):
        return self._handle(0, request, format, resource_id)