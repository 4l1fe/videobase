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

        try:
            ur = UsersRels(**ur_fields)
            ur.rel_type = APP_USER_REL_TYPE_FRIENDS
            ur.save()
        except IntegrityError:
            UsersRels.objects.filter(**ur_fields).update(rel_type=APP_USER_REL_TYPE_FRIENDS)

        if UsersRels.objects.filter(**ur_fr_fields).exists():
            Feed.objects.filter(user=request.user, type=USER_ASK, obj_id=user_friend.id).delete()
            feed, created = Feed.objects.get_or_create(user=self.request.user, type=USER_FRIENDSHIP, obj_id=user_friend.id)
            if not created: feed.save()
        else:
            feed, created = Feed.objects.get_or_create(user=self.request.user, type=USER_ASK, obj_id=user_friend.id)
            if not created: feed.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_NONE)
        Feed.objects.filter(user=request.user, type__in=[USER_FRIENDSHIP, USER_ASK], obj_id=user_friend.id).delete()

        return Response(DEFAULT_REST_API_RESPONSE,status=status.HTTP_200_OK)
        

