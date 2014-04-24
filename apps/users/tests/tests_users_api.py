# coding: utf-8
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from apps.users.constants import APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE,\
    APP_USERS_API_DEFAULT_PER_PAGE, APP_USERS_API_DEFAULT_PAGE
from apps.users.models.api_session import SessionToken, UsersApiSessions
from apps.users.tests.factories import *

import random


class APIUsersFriendShipActionTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_friendship_action'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = "%s %s" % ('X-VB-Token', s_token.key)

    def test_api_users_friendship_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_friendship_401_delete(self):
        response = self.client.delete(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_friendship_200_get(self):
        user = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user.pk
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                                   HTTP_AUTHORIZATION=self.headers)
        flag = UsersRels.objects.filter(user=self.user, user_rel=user).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flag, True)

    def test_api_user_friendship_200_with_rel_delete(self):
        user = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user.pk
        UserRelsFactory.create(user=self.user, user_rel=user)
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                                   HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_friendship_200_without_rel_delete(self):
        user = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user.pk
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                                   HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_friendship_400_bad_user_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                        HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_user_friendship_400_bad_user_delete(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                        HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIUsersGenresTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        genres = []
        films = []
        for i in range(10):
            genres.append(GenreFactory.create())

        for i in range(4):
            films.append(FilmFactory.create(genres=[genres[2*i], genres[2*i+1]]))

        for i in range(4):
            UserFilmsFactory.create(user=self.user, film=films[i])

        self.url_name = 'users_genres'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = "%s %s" % ('X-VB-Token', s_token.key)

    def test_api_users_genres_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_genres_400_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                        HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_genres_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers)
        genres = Genres.objects.filter(genres__users_films__user=self.user).distinct()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(genres)):
            self.assertEqual(response.data[i]['id'], genres[i].pk)
            self.assertEqual(response.data[i]['name'], genres[i].name)


class APIUsersTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.profile = self.user.profile
        self.pic = UserPicsFactory.create(user=self.user)
        self.profile.userpic_id = self.pic.pk
        self.profile.save()
        for i in range(10):
            new_user = UserFactory.create()
            UserRelsFactory.create(user=self.user, user_rel=new_user,
                                   rel_type=random.choice((APP_USER_REL_TYPE_FRIENDS, APP_USER_REL_TYPE_NONE, )))

        for i in range(10):
            CommentsFactory.create(user=self.user)

        genres = []
        films = []
        for i in range(10):
            genres.append(GenreFactory.create())

        for i in range(4):
            films.append(FilmFactory.create(genres=[genres[2*i], genres[2*i+1]]))

        for i in range(4):
            UserFilmsFactory.create(user=self.user, film=films[i])

        self.url_name = 'users'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = "%s %s" % ('X-VB-Token', s_token.key)

    def test_api_users_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_400_get(self):
        pk = User.objects.latest('id').pk
        self.kwargs['user_id'] = int(pk) + 1
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))

    def test_api_users_401_post(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_400_post(self):
        pk = User.objects.latest('id').pk
        self.kwargs['user_id'] = int(pk) + 1
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_200_post_extend_without_reltype(self):
        user = UserFactory.create()
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=headers, data={'extend': True})
        comments_cnt = Comments.objects.filter(user=self.user).count()
        friends_cnt = UsersRels.objects.filter(user=self.user,
                                               rel_type=APP_USER_REL_TYPE_FRIENDS).count()
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        try:
            rel = UsersRels.objects.get(user=user, user_rel=self.user).rel_type
        except:
            rel = APP_USER_REL_TYPE_NONE

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        self.assertEqual(response.data['regdate'], self.user.date_joined)
        self.assertEqual(response.data['friends_cnt'], friends_cnt)
        self.assertEqual(response.data['comments_cnt'], comments_cnt)
        self.assertEqual(response.data['relation'], rel)
        self.assertEqual(response.data['relation'], APP_USER_REL_TYPE_NONE)

    def test_api_users_200_post_extend_with_reltype(self):
        user = UserFactory.create()
        UserRelsFactory.create(user=self.user, user_rel=user, rel_type=APP_USER_REL_TYPE_FRIENDS)
        s_token = SessionToken.objects.create(user=user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=headers, data={'extend': True})
        comments_cnt = Comments.objects.filter(user=self.user).count()
        friends_cnt = UsersRels.objects.filter(user=self.user,
                                               rel_type=APP_USER_REL_TYPE_FRIENDS).count()
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        try:
            rel = UsersRels.objects.get(user=self.user, user_rel=user).rel_type
        except:
            rel = APP_USER_REL_TYPE_NONE

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        self.assertEqual(response.data['regdate'], self.user.date_joined)
        self.assertEqual(response.data['friends_cnt'], friends_cnt)
        self.assertEqual(response.data['comments_cnt'], comments_cnt)
        self.assertEqual(response.data['relation'], rel)
        self.assertEqual(response.data['relation'], APP_USER_REL_TYPE_FRIENDS)

    def test_api_users_200_post_genres(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers, data={'genres': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))

        genres = Genres.objects.filter(genres__users_films__user=self.user)
        for i in range(len(genres)):
            self.assertEqual(response.data['genres'][i]['id'], genres[i].pk)
            self.assertEqual(response.data['genres'][i]['name'], genres[i].name)

    def test_api_users_200_post_friends(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=self.headers, data={'friends': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()
        for i in range(friends.count()):
            self.assertEqual(response.data['friends'][i]['id'], friends[i].pk)
            self.assertEqual(response.data['friends'][i]['name'], friends[i].profile.nickname)
            try:
                pic = UsersPics.objects.get(pk=friends[i].profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['friends'][i]['avatar'], path)

    def test_api_users_200_post_extend_genres_friends(self):
        user = UserFactory.create()
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_AUTHORIZATION=headers, data={'extend': True,
                                                                     'genres': True,
                                                                     'friends': True,
                                                                     })
        comments_cnt = Comments.objects.filter(user=self.user).count()
        friends_cnt = UsersRels.objects.filter(user=self.user,
                                               rel_type=APP_USER_REL_TYPE_FRIENDS).count()
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        try:
            rel = UsersRels.objects.get(user=user, user_rel=self.user).rel_type
        except:
            rel = APP_USER_REL_TYPE_NONE

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.nickname)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        self.assertEqual(response.data['regdate'], self.user.date_joined)
        self.assertEqual(response.data['friends_cnt'], friends_cnt)
        self.assertEqual(response.data['comments_cnt'], comments_cnt)
        self.assertEqual(response.data['relation'], rel)
        self.assertEqual(response.data['relation'], APP_USER_REL_TYPE_NONE)

        genres = Genres.objects.filter(genres__users_films__user=self.user)
        for i in range(len(genres)):
            self.assertEqual(response.data['genres'][i]['id'], genres[i].pk)
            self.assertEqual(response.data['genres'][i]['name'], genres[i].name)

        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()
        for i in range(friends.count()):
            self.assertEqual(response.data['friends'][i]['id'], friends[i].pk)
            self.assertEqual(response.data['friends'][i]['name'], friends[i].profile.nickname)
            try:
                pic = UsersPics.objects.get(pk=friends[i].profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['friends'][i]['avatar'], path)


class APIUsersFriendsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_friends'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        self.friends = []
        for i in range(20):
            new_user = UserFactory.create()
            new_user.profile.userpic_id = UserPicsFactory.create(user=new_user).id
            self.friends.append(new_user)
            UserRelsFactory.create(user=self.user, user_rel=new_user,
                                   rel_type=random.choice((APP_USER_REL_TYPE_FRIENDS,
                                                           APP_USER_REL_TYPE_NONE, )))
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = "%s %s" % ('X-VB-Token', s_token.key)

    def test_api_users_friends_401_post(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_friends_400_bad_user_post(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.post(reverse(self.url_name, kwargs=kw),
                        HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_friends_400_bad_page_post(self):
        page_obj = Paginator(self.friends, APP_USERS_API_DEFAULT_PER_PAGE)
        page_num = page_obj.num_pages + 1
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                    HTTP_AUTHORIZATION=self.headers, data={'page': page_num})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_api_users_friends_200_without_page_post(self):
    #     page_obj = Paginator(self.friends, APP_USERS_API_DEFAULT_PER_PAGE).\
    #         page(APP_USERS_API_DEFAULT_PAGE)
    #     response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
    #                                 HTTP_AUTHORIZATION=self.headers)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['per_page'], APP_USERS_API_DEFAULT_PER_PAGE)
    #     self.assertEqual(response.data['page'], APP_USERS_API_DEFAULT_PAGE)
    #     for i in range(len(page_obj.object_list)):
    #         user = page_obj.object_list[i]
    #         self.assertEqual(response.data['items'][i]['id'], user.pk)
    #         self.assertEqual(response.data['items'][i]['name'], user.profile.nickname)
    #         pic = UsersPics.objects.get(pk=user.profile.userpic_id)
    #         self.assertEqual(response.data['items'][i]['avatar'], pic.image.storage.url(pic.image.name))

    #
    # def test_api_users_friends_200_with_page_post(self):
    #     pass


# TODO: Сделать после исправления vbPerson
# class APIUsersPersonsTestCase(APITestCase):
#     def setUp(self):
#         self.user = UserFactory.create()
#         self.url_name = 'users_persons'
#         self.kwargs = {'format': 'json', 'user_id': self.user.pk}
#         for i in range(10):
#             UserPersonsFatory.create(user=self.user)
#         s_token = SessionToken.objects.create(user=self.user)
#         UsersApiSessions.objects.create(token=s_token)
#         self.headers = "%s %s" % ('X-VB-Token', s_token.key)
#
#     def test_api_users_genres_401_post(self):
#         response = self.client.post(reverse(self.url_name, kwargs=self.kwargs))
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_api_users_genres_400_post(self):
#         pk = User.objects.latest('id').pk
#         kw = self.kwargs.copy()
#         kw['user_id'] = pk + 1
#         response = self.client.post(reverse(self.url_name, kwargs=kw),
#                         HTTP_AUTHORIZATION=self.headers)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_api_users_genres_200_post(self):
#         response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
#                                    HTTP_AUTHORIZATION=self.headers)
#         persons = Persons.objects.filter(users_persons__user=self.user)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         for i in range(len(persons)):
#             self.assertEqual(response.data[i]['id'], persons[i].pk)
#             self.assertEqual(response.data[i]['name'], persons[i].name)

# TODO: Сделать после исправления vbFilms
# class APIUsersFilmsTestCase(APITestCase):
