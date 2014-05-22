# coding: utf-8
from apps.users.models import User, UsersRels, Feed, UsersPics
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json


class UsersFriendshipView(APIView):

    permission_classes = (IsAuthenticated, )

    def _get_avatar_url(self, u):
        try:
            a = UsersPics.objects.get(user=u).image
            return a.storage.url(a.name)
        except:
            return ''

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        ur_fields = {'user': request.user, 'user_rel': user_friend, 'rel_type': APP_USER_REL_TYPE_FRIENDS}
        ur_fr_fields = {'user': user_friend, 'user_rel': request.user, 'rel_type': APP_USER_REL_TYPE_FRIENDS}
        avatar_url = self._get_avatar_url(user_friend)
        obj_val = json.dumps({'id': user_friend.id, 'name': user_friend.username, 'avatar': avatar_url})
        ur, created = UsersRels.objects.create(**ur_fields)
        if not created:
            ur.rel_type = ur_fields['rel_type']
            ur.save()

        if UsersRels.objects.filter(**ur_fr_fields).exists():
            Feed.objects.filter(user=request.user, type='user-a', object=obj_val).delete()
            f, created = Feed.objects.get_or_create(user=request.user, type='user-f', object=obj_val)
            if not created: f.save()
        else:
            f, created = Feed.objects.get_or_create(user=request.user, type='user-a', object=obj_val)
            if not created: f.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        avatar_url = self._get_avatar_url(user_friend)
        obj_val = json.dumps({'id': user_friend.id, 'name': user_friend.username, 'avatar': avatar_url})
        UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_NONE)
        Feed.objects.filter(user=request.user, type='user-f', object=obj_val).delete()
        Feed.objects.filter(user=request.user, type='user-a', object=obj_val).delete()

        return Response(status=status.HTTP_200_OK)