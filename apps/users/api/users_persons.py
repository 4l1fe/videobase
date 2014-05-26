# coding: utf-8

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.films.models import Persons
from apps.films.api.serializers import vbPerson
from apps.films.constants import APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, APP_PERSON_PRODUCER, APP_PERSON_SCRIPTWRITER
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE

persons_type = {
    'a': (APP_PERSON_ACTOR, ),
    'p': (APP_PERSON_PRODUCER, ),
    'd': (APP_PERSON_DIRECTOR, ),
    's': (APP_PERSON_SCRIPTWRITER, ),
    'all': (APP_PERSON_DIRECTOR, APP_PERSON_SCRIPTWRITER,
            APP_PERSON_ACTOR, APP_PERSON_DIRECTOR, ),
}


class UsersPersonsView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        page = request.QUERY_PARAMS.get('page', APP_USERS_API_DEFAULT_PAGE)
        per_page = request.QUERY_PARAMS.get('per_page', APP_USERS_API_DEFAULT_PER_PAGE)
        type_ = request.QUERY_PARAMS.get('type', 'all')

        try:
            ptype = persons_type[type_]
        except KeyError as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        persons = Persons.objects.filter(up_persons_rel__user=user, pf_persons_rel__p_type__in=ptype)
        try:
            page = Paginator(persons, per_page).page(page)
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        serializer = vbPerson(page.object_list, user=user, many=True)
        result = {
            'page': page.number,
            'per_page': page.paginator.per_page,
            'items': serializer.data,
            'total_cnt': page.paginator.count,
        }

        return Response(result, status=status.HTTP_200_OK)
