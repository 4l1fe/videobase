# coding: utf-8
from apps.users.models import User, UsersRels
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

import datetime


class UsersFriendshipView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return Response({'error': e.message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        UsersRels.objects.create(user=request.user,
                                 user_rel=user,
                                 rel_type=APP_USER_REL_TYPE_FRIENDS)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return Response({'error': e.message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        current_user = request.user
        try:
            rel = current_user.rels.get(user_rel=user)
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        rel.rel_type = APP_USER_REL_TYPE_NONE
        rel.updated = datetime.datetime.now()
        rel.save()
        return Response(status=status.HTTP_200_OK)
