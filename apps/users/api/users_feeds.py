# coding: utf-8

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.films.models import UsersFilms, UsersPersons

from apps.users.models import User, Feed, UsersRels
from apps.users.api.serializers import vbFeedElement
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE

feed_type_api = ['u', 'f', 'all']


class UsersFeedsView(APIView):

    def get(self, request, user_id, format=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except Exception, e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        page = request.QUERY_PARAMS.get('page', APP_USERS_API_DEFAULT_PAGE)
        per_page = request.QUERY_PARAMS.get('per_page', APP_USERS_API_DEFAULT_PER_PAGE)

        result = self.validation(page, per_page)
        if isinstance(result, Exception):
            return Response({'e': result.message}, status=status.HTTP_400_BAD_REQUEST)

        feed_type = request.QUERY_PARAMS.get('type', 'u')
        if not feed_type in feed_type_api:
            return Response({'e': u'Неизвестный тип фида'}, status=status.HTTP_400_BAD_REQUEST)

        # Init data
        user_id = user.id
        page, per_page = result
        offset = (page - 1) * per_page

        if feed_type == 'u':
            uf, up = self.get_users_and_persons_info(user_id)
            o_feed, count = Feed.get_feeds_by_user(user_id, uf=uf, up=up, count=True, offset=offset, limit=per_page)

        elif feed_type == 'f':
            ur = self.get_rels_info(user_id)
            o_feed, count = Feed.get_feeds_by_user_friends(ur=ur, count=True, offset=offset, limit=per_page)

        else:
            uf, up = self.get_users_and_persons_info(user_id)
            ur = self.get_rels_info(user_id)
            o_feed, count = Feed.get_feeds_by_user_all(user_id, uf=uf, up=up, ur=ur,
                                                        count=True, offset=offset, limit=per_page)

        # Сериализуем данные
        try:
            serializer = vbFeedElement(o_feed, many=True).data
        except Exception as e:
            return Response({'e': e.message}, status=status.HTTP_400_BAD_REQUEST)

        result = {
            'per_page': per_page,
            'page': page,
            'total_cnt': count,
            'items': serializer,
        }

        return Response(result, status=status.HTTP_200_OK)

    def get_users_and_persons_info(self, user_id):
        # Список подписок на фильм
        uf = UsersFilms.get_subscribed_films_by_user(user_id, flat=True)

        # Список подписок на персону
        up = UsersPersons.get_subscribed_persons_by_user(user_id, flat=True)

        return uf, up


    def get_rels_info(self, user_id):
        # Список друзей пользователя
        return UsersRels.get_all_friends_user(user_id, flat=True)


    def validation(self, page, per_page):
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = APP_USERS_API_DEFAULT_PAGE

        if page < APP_USERS_API_DEFAULT_PAGE:
            page = APP_USERS_API_DEFAULT_PAGE

        try:
            per_page = int(per_page)
        except (TypeError, ValueError):
            per_page = APP_USERS_API_DEFAULT_PER_PAGE

        if 0 < per_page > APP_USERS_API_DEFAULT_PER_PAGE:
            per_page = APP_USERS_API_DEFAULT_PER_PAGE

        return page, per_page
