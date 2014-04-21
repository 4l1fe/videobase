# coding: utf-8
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.constants import APP_USER_REL_TYPE_FRIENDS
from apps.users.models import User
from apps.users.api.serializers import vbUser


class UsersFriendsView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist as e:
            return Response({'e': e.message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        page = request.DATA.get('page', 1)
        per_page = request.DATA.get('per_page', 10)

        persons = User.objects.filter(rels__user=user,
                                      rels__rel_type=APP_USER_REL_TYPE_FRIENDS)
        try:
            page = Paginator(persons, per_page).page(page)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbUser(page.object_list, many=True)
        result = {
            'page': page.number,
            'per_page': page.paginator.per_page,
            'items': serializer.data,
            'total_cnt': page.paginator.count,
        }

        return Response(result, status=status.HTTP_200_OK)
