# coding: utf-8

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import UsersFilms, UsersPersons

from apps.users.models import User, Feed
from apps.users.api.serializers import vbFeedElement
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_FEED_PER_PAGE


class UsersFeedsView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception, e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        user_id = user.id
        page = request.QUERY_PARAMS.get('page', APP_USERS_API_DEFAULT_PAGE)
        per_page = request.QUERY_PARAMS.get('per_page', APP_USERS_API_DEFAULT_FEED_PER_PAGE)

        # Список подписок на фильм
        uf = UsersFilms.get_subscribed_films_by_user(user_id, flat=True)

        # Список подписок на персону
        up = UsersPersons.get_subscribed_persons_by_user(user_id, flat=True)

        o_feed = Feed.get_feeds_by_user(user_id, uf=uf, up=up)
        try:
            page = Paginator(o_feed, per_page).page(page)

            # Сериализуем данные
            serializer = vbFeedElement(page.object_list, request=self.request, many=True)
            result = serializer.data
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
