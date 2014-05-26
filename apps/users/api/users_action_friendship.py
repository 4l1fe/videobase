# coding: utf-8
from apps.users.models import User, UsersRels, Feed, UsersPics
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class UsersFriendshipView(APIView):

    permission_classes = (IsAuthenticated, )

    def _get_avatar_url(self, u):
        try:
            a = UsersPics.objects.get(user=u).image
            return a.storage.url(a.name)
        except:
            return ''

    def _update_or_create_feed(self, type_, obj_val):
        ffeeds = Feed.objects.filter(user=self.request.user, type=type_)
        feeds = [f for f in ffeeds]
        objs = [f.object for f in ffeeds]
        try:
            f = feeds[objs.index(obj_val)]
            f.save()
        except ValueError:
            Feed.objects.create(user=self.request.user, type=type_, object=obj_val)

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        ur_fields = {'user': request.user, 'user_rel': user_friend}
        ur_fr_fields = {'user': user_friend, 'user_rel': request.user, 'rel_type': APP_USER_REL_TYPE_FRIENDS}
        avatar_url = self._get_avatar_url(user_friend)
        obj_val = {'id': user_friend.id, 'name': user_friend.username, 'avatar': avatar_url}

        try:
            ur = UsersRels(**ur_fields)
            ur.rel_type = APP_USER_REL_TYPE_FRIENDS
            ur.save()
        except IntegrityError:
            UsersRels.objects.filter(**ur_fields).update(rel_type=APP_USER_REL_TYPE_FRIENDS)

        if UsersRels.objects.filter(**ur_fr_fields).exists():
            for f in Feed.objects.filter(user=request.user, type='user-a').iterator():
                if f.object == obj_val: f.delete()
            self._update_or_create_feed('user-f', obj_val)
        else:
            self._update_or_create_feed('user-a', obj_val)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        obj_val = {'id': user_friend.id, 'name': user_friend.username}
        UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_NONE)
        for f in Feed.objects.filter(user=request.user, type='user-f').iterator():
            if f.object == obj_val: f.delete()
        for f in Feed.objects.filter(user=request.user, type='user-a').iterator():
            if f.object == obj_val: f.delete()
        return Response(status=status.HTTP_200_OK)