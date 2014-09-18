# coding: utf-8
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS
from apps.users.models import User
from apps.users.api.serializers import vbUser
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE


class UsersFriendsView(APIView):

    def post(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        page = request.DATA.get('page', APP_USERS_API_DEFAULT_PAGE)
        per_page = request.DATA.get('per_page', APP_USERS_API_DEFAULT_PER_PAGE)

        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, user.pk]).all()
        try:
            page = Paginator(friends, per_page).page(page)
        except Exception as e:
            return Response({'e': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbUser(page.object_list, many=True)
        result = {
            'page': page.number,
            'per_page': page.paginator.per_page,
            'items': serializer.data,
            'total_cnt': page.paginator.count,
        }

        return Response(result, status=status.HTTP_200_OK)
