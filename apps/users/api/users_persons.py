# coding: utf-8

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Persons
from apps.films.api.serializers import vbPerson


class UsersPersonsView(APIView):

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
        type = request.DATA.get('type', 'all')

        persons = Persons.objects.filter(users_persons__user=user)
        try:
            page = Paginator(persons, per_page).page(page)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbPerson(page.object_list, many=True)
        result = {
            'page': page.number,
            'per_page': page.paginator.per_page,
            'items': serializer.data,
            'total_cnt': page.paginator.count,
        }

        return Response(result, status=status.HTTP_200_OK)