# coding: utf-8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django.db.models import Q
from videobase.settings import DEFAULT_REST_API_RESPONSE
from apps.users.models import User, UsersRels, Feed
from apps.users.constants import (APP_USER_REL_TYPE_NONE,
                                  USER_ASK, USER_FRIENDSHIP,
                                  APP_USER_REL_TYPE_SEND_NOT_RECEIVED,
                                  APP_USER_REL_TYPE_FRIENDS
)


class UsersFriendshipView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, format=None, *args, **kwargs):

        try:
            user_friend = User.objects.get(pk=user_id)

            response_template = {'id':user_friend.id,
                             'name':user_friend.get_full_name() }

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if UsersRels.objects.filter(user_id=user_friend.id, user_rel_id=request.user.id,
                                                rel_type=APP_USER_REL_TYPE_SEND_NOT_RECEIVED).exists():  # если есть встречная заявка
            if UsersRels.objects.filter(user_rel_id=user_friend.id, user_id=request.user.id,
                                                rel_type=APP_USER_REL_TYPE_SEND_NOT_RECEIVED).exists():
                return Response(dict(relation=APP_USER_REL_TYPE_FRIENDS,
                                 **response_template),
                          status=status.HTTP_200_OK)
            else:
                return Response(dict(relation=APP_USER_REL_TYPE_SEND_NOT_RECEIVED,
                                 **response_template),
                          status=status.HTTP_200_OK)
            
    def post(self, request, user_id, format=None):
        try:
            user_friend = User.objects.get(pk=user_id)

            response_template = {'id':user_friend.id,
                                 'name':user_friend.get_full_name()
            }

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ur = UsersRels(user=request.user, user_rel=user_friend)
            ur.rel_type = APP_USER_REL_TYPE_SEND_NOT_RECEIVED
            ur.save()

        except IntegrityError:
            UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_SEND_NOT_RECEIVED)

        if UsersRels.objects.filter(user_id=user_friend.id, user_rel_id=request.user.id,
                                                rel_type=APP_USER_REL_TYPE_SEND_NOT_RECEIVED).exists():  # если есть встречная заявка
            Feed.objects.filter(Q(user=request.user, type=USER_ASK, obj_id=user_friend.id)
                                | Q(user=user_friend, type=USER_ASK, obj_id=request.user.id)).delete()
            feed, created = Feed.objects.get_or_create(user=request.user, type=USER_FRIENDSHIP, obj_id=user_friend.id)
            if not created: feed.save()
            feed, created = Feed.objects.get_or_create(user=user_friend, type=USER_FRIENDSHIP, obj_id=request.user.id)
            if not created: feed.save()

            return Response(dict(
                relation=APP_USER_REL_TYPE_FRIENDS, **response_template),
                          status=status.HTTP_200_OK)
        else:
            feed, created = Feed.objects.get_or_create(user=request.user, type=USER_ASK, obj_id=user_friend.id)
            if not created: feed.save()

            return Response(dict(relation=APP_USER_REL_TYPE_SEND_NOT_RECEIVED,
                                 **response_template),
                          status=status.HTTP_200_OK)


    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user_friend = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        UsersRels.objects.filter(user=request.user, user_rel=user_friend).update(rel_type=APP_USER_REL_TYPE_NONE)
        Feed.objects.filter(user=request.user, type__in=[USER_FRIENDSHIP, USER_ASK], obj_id=user_friend.id).delete()
        Feed.objects.filter(user=user_friend, type=USER_FRIENDSHIP, obj_id=request.user.id).update(type=USER_ASK)

        return Response(DEFAULT_REST_API_RESPONSE,status=status.HTTP_200_OK)