# coding: utf-8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from videobase.settings import DEFAULT_REST_API_RESPONSE
from apps.users.models import User, UsersRels, Feed, UsersPics
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE, \
    USER_ASK, USER_FRIENDSHIP


class UsersFriendshipView(APIView):

    permission_classes = (IsAuthenticated, )

    def _get_avatar_url(self, u):
        try:
            a = UsersPics.objects.get(user=u).image
            return a.storage.url(a.name)
        except:
            return ''

    def _update_or_create_feed(self, type_, obj_id):
        if Feed.objects.filter(user=self.request.user, type=type_, obj_id=obj_id).exists():
            Feed.objects.filter(user=self.request.user, type=type_, obj_id=obj_id).update(obj_id=obj_id)
        else:
            Feed.objects.create(user=self.request.user, type=type_, obj_id=obj_id)

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        ur_fields = {
            'user': request.user,
            'user_rel': user_friend
        }

        ur_fr_fields = {
            'user': user_friend,
            'user_rel': request.user,
            'rel_type': APP_USER_REL_TYPE_FRIENDS
        }

        # avatar_url = self._get_avatar_url(user_friend)
        # obj_val = {
        #     'id': user_friend.id,
        #     'name': user_friend.username,
        #     'avatar': avatar_url
        # }

        try:
            ur = UsersRels(**ur_fields)
            ur.rel_type = APP_USER_REL_TYPE_FRIENDS
            ur.save()
        except IntegrityError:
            UsersRels.objects.filter(**ur_fields).update(rel_type=APP_USER_REL_TYPE_FRIENDS)

        if UsersRels.objects.filter(**ur_fr_fields).exists():
            Feed.objects.filter(user=request.user, type=USER_ASK, obj_id=request.user.id).delete()
            self._update_or_create_feed(USER_FRIENDSHIP, request.user.id)
        else:
            self._update_or_create_feed(USER_ASK, request.user.id)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_NONE)
        Feed.objects.filter(user=request.user, type__in=[USER_FRIENDSHIP, USER_ASK], obj_id=user_friend).delete()

        return Response(DEFAULT_REST_API_RESPONSE,status=status.HTTP_200_OK)
        

