# coding: utf-8
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.test import APITestCase, APISimpleTestCase
from rest_framework.reverse import reverse
from apps.films.constants import (APP_FILM_SERIAL, APP_USERFILM_STATUS_PLAYLIST, APP_PERSON_DIRECTOR,
                                  APP_PERSON_ACTOR, APP_PERSON_SCRIPTWRITER, APP_PERSON_PRODUCER,
                                  APP_USERFILM_SUBS_TRUE)
from apps.users.constants import (APP_USER_REL_TYPE_NONE, APP_USER_REL_TYPE_SEND_NOT_RECEIVED,
                                  APP_USERS_API_DEFAULT_PER_PAGE, APP_USERS_API_DEFAULT_PAGE)
from apps.users.models import SessionToken
from apps.users.tests.factories_users_api import *
from apps.users.api.users_persons import persons_type
from apps.users.constants import USER_ASK, USER_FRIENDSHIP
from apps.users.constants import APP_USER_REL_TYPE_FRIENDS

import random


class APIUsersFriendShipActionTestCase(APISimpleTestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_api:users_friendship_action'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        s_token = SessionToken.objects.create(user=self.user)
        self.headers = s_token.key

    def test_api_users_friendship_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_friendship_401_delete(self):
        response = self.client.delete(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_friendship_200_get(self):
        user_friend = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user_friend.pk
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                                   HTTP_X_MI_SESSION=self.headers)
        flag = UsersRels.objects.filter(user=self.user, user_rel=user_friend).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flag, True)
        feed = Feed.objects.last()
        self.assertEqual(feed.user, self.user)
        self.assertEqual(feed.type, USER_ASK)
        self.assertEqual(feed.obj_id, user_friend.id)

    def test_api_user_friendship_confirm_200_get(self):
        user_friend = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user_friend.pk
        UserRelsFactory.create(user=user_friend, user_rel=self.user, rel_type=APP_USER_REL_TYPE_SEND_NOT_RECEIVED)
        FeedFactory.create(user=user_friend, obj_id=self.user.id, type=USER_ASK)
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                                   HTTP_X_MI_SESSION=self.headers)
        feed = Feed.objects.order_by('-created')[1]
        self.assertEqual(feed.user, self.user)
        self.assertEqual(feed.type, USER_FRIENDSHIP)
        self.assertEqual(feed.obj_id, user_friend.id)

    def test_api_user_friendship_200_with_rel_delete(self):
        user_friend = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user_friend.pk
        UserRelsFactory.create(user=self.user, user_rel=user_friend)
        FeedFactory.create(user=self.user, type=USER_ASK, obj_id=user_friend.id)
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                                   HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Feed.objects.filter(user=self.user).exists())

    def test_api_user_friendship_200_without_rel_delete(self):
        user = UserFactory.create()
        kw = self.kwargs.copy()
        kw['user_id'] = user.pk
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                                   HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_user_friendship_400_bad_user_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw),
                        HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_user_friendship_400_bad_user_delete(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.delete(reverse(self.url_name, kwargs=kw),
                        HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIUsersGenresTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        genres = []
        films = []
        for i in range(10):
            genres.append(Genres.add_root(instance=GenreFactory.build()))

        for i in range(4):
            films.append(FilmFactory.create(genres=[genres[2*i], genres[2*i+1]]))

        for i in range(4):
            UserFilmsFactory.create(user=self.user, film=films[i])

        self.url_name = 'users_api:users_genres'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}

    def test_api_users_genres_400_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_genres_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        genres = Genres.get_all_genres(get_values=False).filter(genres__uf_films_rel__user=self.user).distinct()
        genres = [i.get_root() for i in set(genres)]
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
            genres.append(Genres.add_root(instance=GenreFactory.build()))

        for i in range(4):
            films.append(FilmFactory.create(genres=[genres[2*i], genres[2*i+1]]))

        for i in range(4):
            UserFilmsFactory.create(user=self.user, film=films[i])

        self.url_name = 'users_api:users'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        s_token = SessionToken.objects.create(user=self.user)
        self.headers = s_token.key

    def test_api_users_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_400_get(self):
        pk = User.objects.latest('id').pk
        self.kwargs['user_id'] = int(pk) + 1
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.get_name())
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))

    def test_api_users_401_post(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_users_400_post(self):
        pk = User.objects.latest('id').pk
        self.kwargs['user_id'] = int(pk) + 1
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_200_post_extend_without_reltype(self):
        user = UserFactory.create()

        s_token = SessionToken.objects.create(user=self.user)
        headers = s_token.key

        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=headers, data={'extend': True})

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
        self.assertEqual(response.data['name'], self.profile.get_name())
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
        headers = s_token.key

        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=headers, data={'extend': True})

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
        self.assertEqual(response.data['name'], self.profile.get_name())
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        self.assertEqual(response.data['regdate'], self.user.date_joined)
        self.assertEqual(response.data['friends_cnt'], friends_cnt)
        self.assertEqual(response.data['comments_cnt'], comments_cnt)
        self.assertEqual(response.data['relation'], rel)
        self.assertEqual(response.data['relation'], APP_USER_REL_TYPE_FRIENDS)

    def test_api_users_200_post_genres(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=self.headers, data={'genres': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.get_name())
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))

        genres = Genres.objects.filter(genres__uf_films_rel__user=self.user)
        for i in range(len(genres)):
            self.assertEqual(response.data['genres'][i]['id'], genres[i].pk)
            self.assertEqual(response.data['genres'][i]['name'], genres[i].name)

    def test_api_users_200_post_friends(self):
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=self.headers, data={'friends': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.pk)
        self.assertEqual(response.data['name'], self.profile.get_name())
        pic = UsersPics.objects.get(pk=self.profile.userpic_id)
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()
        for i in range(friends.count()):
            self.assertEqual(response.data['friends'][i]['id'], friends[i].pk)
            self.assertEqual(response.data['friends'][i]['name'], friends[i].profile.get_name())
            try:
                pic = UsersPics.objects.get(pk=friends[i].profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['friends'][i]['avatar'], path)

    def test_api_users_200_post_extend_genres_friends(self):
        user = UserFactory.create()

        s_token = SessionToken.objects.create(user=self.user)
        headers = s_token.key

        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                   HTTP_X_MI_SESSION=headers,
                                   data={
                                       'extend': True,
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
        self.assertEqual(response.data['name'], self.profile.get_name())
        self.assertEqual(response.data['avatar'], pic.image.storage.url(pic.image.name))
        self.assertEqual(response.data['regdate'], self.user.date_joined)
        self.assertEqual(response.data['friends_cnt'], friends_cnt)
        self.assertEqual(response.data['comments_cnt'], comments_cnt)
        self.assertEqual(response.data['relation'], rel)
        self.assertEqual(response.data['relation'], APP_USER_REL_TYPE_NONE)

        genres = Genres.objects.filter(genres__uf_films_rel__user=self.user)
        for i in range(len(genres)):
            self.assertEqual(response.data['genres'][i]['id'], genres[i].pk)
            self.assertEqual(response.data['genres'][i]['name'], genres[i].name)

        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()
        for i in range(friends.count()):
            self.assertEqual(response.data['friends'][i]['id'], friends[i].pk)
            self.assertEqual(response.data['friends'][i]['name'], friends[i].profile.get_name())
            try:
                pic = UsersPics.objects.get(pk=friends[i].profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['friends'][i]['avatar'], path)


class APIUsersFriendsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_api:users_friends'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        self.friends = []
        for i in range(20):
            new_user = UserFactory.create()
            new_user.profile.userpic_id = UserPicsFactory.create(user=new_user).id
            self.friends.append(new_user)
            UserRelsFactory.create(user=self.user, user_rel=new_user,
                                   rel_type=random.choice((APP_USER_REL_TYPE_FRIENDS,
                                                           APP_USER_REL_TYPE_NONE, )))

    def test_api_users_friends_400_bad_user_post(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.post(reverse(self.url_name, kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_friends_400_bad_page_post(self):
        page_obj = Paginator(self.friends, APP_USERS_API_DEFAULT_PER_PAGE)
        page_num = page_obj.num_pages + 1
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs),
                                    data={'page': page_num})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_friends_200_without_page_post(self):
        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()
        page_obj = Paginator(friends, APP_USERS_API_DEFAULT_PER_PAGE).\
            page(APP_USERS_API_DEFAULT_PAGE)
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['per_page'], APP_USERS_API_DEFAULT_PER_PAGE)
        self.assertEqual(response.data['page'], APP_USERS_API_DEFAULT_PAGE)
        for i in range(len(page_obj.object_list)):
            user = page_obj.object_list[i]
            self.assertEqual(response.data['items'][i]['id'], user.pk)
            self.assertEqual(response.data['items'][i]['name'], user.profile.get_name())
            try:
                pic = UsersPics.objects.get(pk=user.profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['items'][i]['avatar'], path)

    def test_api_users_friends_200_with_page_post(self):
        friends = User.objects.extra(
            where=['id IN (SELECT "user_rel_id" FROM "auth_user" INNER JOIN "users_rels" ON ( "auth_user"."id" = "users_rels"."user_id" ) WHERE ("users_rels"."rel_type" =%s  AND "users_rels"."user_id" = %s ))'],
            params=[APP_USER_REL_TYPE_FRIENDS, self.user.pk]).all()

        page_obj = Paginator(friends, 5).page(2)
        response = self.client.post(reverse(self.url_name, kwargs=self.kwargs), data={'per_page': 5, 'page': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['per_page'], 5)
        self.assertEqual(response.data['page'], 2)

        for i in range(len(page_obj.object_list)):
            user = page_obj.object_list[i]
            self.assertEqual(response.data['items'][i]['id'], user.pk)
            self.assertEqual(response.data['items'][i]['name'], user.profile.get_name())
            try:
                pic = UsersPics.objects.get(pk=user.profile.userpic_id)
                path = pic.image.storage.url(pic.image.name)
            except:
                path = ''
            self.assertEqual(response.data['items'][i]['avatar'], path)


class APIUsersPersonsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_api:users_persons'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        for i in range(10):
            UserPersonsFatory.create(user=self.user)
        persons = Persons.objects.all()
        for person in persons:
            PersonsFilmsFactory.create(person=person, p_type=random.choice((
                APP_PERSON_PRODUCER, APP_PERSON_SCRIPTWRITER,
                APP_PERSON_DIRECTOR, APP_PERSON_ACTOR, )))

    def test_api_users_genres_400_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_genres_200_post(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs))
        ftype = persons_type['all']
        persons = Persons.objects.filter(up_persons_rel__user=self.user,
                                         pf_persons_rel__p_type__in=ftype)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(persons)):
            sub = UsersPersons.objects.get(person=persons[i], user=self.user).subscribed
            self.assertEqual(response.data['items'][i]['id'], persons[i].pk)
            self.assertEqual(response.data['items'][i]['name'], persons[i].name)
            self.assertEqual(response.data['items'][i]['photo'], persons[i].photo.url)
            self.assertEqual(response.data['items'][i]['relation'], sub)
            self.assertEqual(response.data['items'][i]['birthdate'], persons[i].birthdate)
            self.assertEqual(response.data['items'][i]['birthplace'][0], persons[i].city.name)
            self.assertEqual(response.data['items'][i]['birthplace'][1], persons[i].city.country.name)

    def test_api_users_genres_with_type_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   data={'type': 'a'})
        ftype = persons_type['a']
        persons = Persons.objects.filter(up_persons_rel__user=self.user, pf_persons_rel__p_type__in=ftype)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(persons)):
            sub = UsersPersons.objects.get(person=persons[i], user=self.user).subscribed
            self.assertEqual(response.data['items'][i]['id'], persons[i].pk)
            self.assertEqual(response.data['items'][i]['name'], persons[i].name)
            self.assertEqual(response.data['items'][i]['photo'], persons[i].photo.url)
            self.assertEqual(response.data['items'][i]['relation'], sub)
            self.assertEqual(response.data['items'][i]['birthdate'], persons[i].birthdate)
            self.assertEqual(response.data['items'][i]['birthplace'][0], persons[i].city.name)
            self.assertEqual(response.data['items'][i]['birthplace'][1], persons[i].city.country.name)

    def test_api_users_genres_with_bad_type_200_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   data={'type': '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIUsersFilmsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.url_name = 'users_api:users_films'
        self.kwargs = {'format': 'json', 'user_id': self.user.pk}
        films = []
        for i in range(10):
            film = FilmFactory.create(type=random.choice((APP_FILM_SERIAL,
                                                          APP_FILM_FULL_FILM)))
            films.append(film)
            content = ContetsFactory.create(film=film)
            LocationsFactory.create(content=content)

        for i in range(10):
            UserFilmsFactory.create(user=self.user, status=APP_USERFILM_STATUS_PLAYLIST, film=films[i], subscribed=APP_USERFILM_SUBS_TRUE)

    def test_api_users_films_400_get(self):
        pk = User.objects.latest('id').pk
        kw = self.kwargs.copy()
        kw['user_id'] = pk + 1
        response = self.client.get(reverse(self.url_name, kwargs=kw))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_users_films_200_all_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs),
                                   data={'type': 'all'})
        ftype = [APP_FILM_SERIAL, APP_FILM_FULL_FILM]
        films = Films.objects.filter(uf_films_rel__user=self.user, type__in=ftype,
                                     uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), len(films))
        for i in range(len(films)):
            loc = Locations.objects.get(content__film=films[i])
            self.assertEqual(response.data['items'][i]['id'], films[i].pk)
            self.assertEqual(response.data['items'][i]['name'], films[i].name)
            self.assertEqual(response.data['items'][i]['name_orig'], films[i].name_orig)
            self.assertEqual(response.data['items'][i]['releasedate'], films[i].release_date)
            self.assertEqual(response.data['items'][i]['duration'], films[i].duration)
            self.assertEqual(response.data['items'][i]['locations'][0]['type'], loc.type)
            self.assertEqual(response.data['items'][i]['locations'][0]['lang'], loc.lang)
            self.assertEqual(response.data['items'][i]['locations'][0]['quality'], loc.quality)
            self.assertEqual(response.data['items'][i]['locations'][0]['price'], loc.price)
            self.assertEqual(response.data['items'][i]['locations'][0]['subtitles'], loc.subtitles)
            self.assertEqual(response.data['items'][i]['locations'][0]['price_type'], loc.price_type)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons_cnt)

    def test_api_users_films_200_serial_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs), data={'type': 's'})
        ftype = [APP_FILM_SERIAL]
        films = Films.objects.filter(uf_films_rel__user=self.user, type__in=ftype,
                                     uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), len(films))
        for i in range(len(films)):
            loc = Locations.objects.get(content__film=films[i])
            self.assertEqual(response.data['items'][i]['id'], films[i].pk)
            self.assertEqual(response.data['items'][i]['name'], films[i].name)
            self.assertEqual(response.data['items'][i]['name_orig'], films[i].name_orig)
            self.assertEqual(response.data['items'][i]['releasedate'], films[i].release_date)
            self.assertEqual(response.data['items'][i]['duration'], films[i].duration)
            self.assertEqual(response.data['items'][i]['locations'][0]['type'], loc.type)
            self.assertEqual(response.data['items'][i]['locations'][0]['lang'], loc.lang)
            self.assertEqual(response.data['items'][i]['locations'][0]['quality'], loc.quality)
            self.assertEqual(response.data['items'][i]['locations'][0]['price'], loc.price)
            self.assertEqual(response.data['items'][i]['locations'][0]['subtitles'], loc.subtitles)
            self.assertEqual(response.data['items'][i]['locations'][0]['price_type'], loc.price_type)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons_cnt)

    def test_api_users_films_200_full_film_get(self):
        response = self.client.get(reverse(self.url_name, kwargs=self.kwargs), data={'type': 'f'})
        films = Films.objects.filter(uf_films_rel__user=self.user,
                                     type__in=[APP_FILM_FULL_FILM],
                                     uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), len(films))
        for i in range(len(films)):
            loc = Locations.objects.get(content__film=films[i])
            self.assertEqual(response.data['items'][i]['id'], films[i].pk)
            self.assertEqual(response.data['items'][i]['name'], films[i].name)
            self.assertEqual(response.data['items'][i]['name_orig'], films[i].name_orig)
            self.assertEqual(response.data['items'][i]['releasedate'], films[i].release_date)
            self.assertEqual(response.data['items'][i]['duration'], films[i].duration)
            self.assertEqual(response.data['items'][i]['locations'][0]['type'], loc.type)
            self.assertEqual(response.data['items'][i]['locations'][0]['lang'], loc.lang)
            self.assertEqual(response.data['items'][i]['locations'][0]['quality'], loc.quality)
            self.assertEqual(response.data['items'][i]['locations'][0]['price'], loc.price)
            self.assertEqual(response.data['items'][i]['locations'][0]['subtitles'], loc.subtitles)
            self.assertEqual(response.data['items'][i]['locations'][0]['price_type'], loc.price_type)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb)
            self.assertEqual(response.data['items'][i]['ratings']['imdb'][0], films[i].rating_imdb_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk)
            self.assertEqual(response.data['items'][i]['ratings']['kp'][0], films[i].rating_kinopoisk_cnt)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons)
            self.assertEqual(response.data['items'][i]['ratings']['cons'][0], films[i].rating_cons_cnt)
