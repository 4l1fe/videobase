# coding: utf-8
import datetime

from pytils import numeral
from django.db import transaction
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, HttpResponseServerError, Http404
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from social.apps.django_app.default.models import UserSocialAuth
from rest_framework.authtoken.models import Token

from tasks import send_template_mail
from apps.users.models import Feed
from apps.users.api.serializers import vbUser, vbFeedElement, vbUserProfile
from apps.users.forms import CustomRegisterForm, UsersProfileForm
from apps.users.api.utils import create_new_session
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE,\
    APP_SUBJECT_TO_RESTORE_PASSWORD
from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_ACTOR, APP_USERFILM_SUBS_TRUE
from apps.films.api.serializers import vbFilm, vbPerson
from utils.common import url_with_querystring
from utils.auth.views import View
from utils.noderender import render_page


HOST = 'vsevi.ru'


class RegisterUserView(View):

    def get(self, *args, **kwargs):
        return HttpResponse(render_page('register', {}))

    @transaction.commit_manually
    def post(self, *args, **kwargs):
        register_form = CustomRegisterForm(data=self.request.POST)
        if register_form.is_valid():
            user = register_form.save()
            kw = {
                'token': user.auth_token.key,
                '_': timezone.now().date().strftime("%H%M%S"),
            }

            url_redirect = url_with_querystring(reverse('tokenize'), **kw)
            # url = "http://{host}{url}".format(host=self.request.get_host(), url=url_redirect)
            # context = {'user': user, 'redirect_url': url}
            #
            # kw = dict(subject=APP_SUBJECT_TO_CONFIRM_REGISTER,
            #           tpl_name='confirmation_register.html',
            #           context=context,
            #           to=[user.email])
            # send_template_mail.apply_async(kwargs=kw)

            transaction.commit()
            return redirect(url_redirect)

        else:
            transaction.rollback()
            resp_dict = {'error': dict(((i[0], i[1][0]) for i in register_form.errors.items()))}
            return HttpResponse(render_page('register', resp_dict))


class LoginUserView(View):

    def get(self, *args, **kwargs):
        response = HttpResponse(render_page('login', {}))
        response.delete_cookie("x-session")
        response.delete_cookie("x-token")
        return response

    def post(self, *args, **kwargs):
        login_form = AuthenticationForm(data=self.request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            kw = {
                'token': user.auth_token.key,
                '_': timezone.now().date().strftime("%H%M%S")
            }
            if self.request.META['HTTP_HOST'] == HOST and not HOST+'/login' in self.request.META['HTTP_REFERER']:
                kw.update(back_url=self.request.META['HTTP_REFERER'])
            url = url_with_querystring(reverse('tokenize'), **kw)
            return HttpResponseRedirect(url)

        else:
            return HttpResponse(render_page('login', {'error': u'Введите корректный логин или пароль'}))


class UserLogoutView(View):

    def get(self, request, **kwargs):
        response = HttpResponseRedirect(reverse('index_view'))
        response.delete_cookie("x-session")
        response.delete_cookie("x-token")
        response.delete_cookie("sessionid")
        return response


class TokenizeView(View):

    @never_cache
    def get(self, *args, **kwargs):
        back_url = self.request.GET['back_url'] if 'back_url' in self.request.GET else reverse('index_view')
        token = self.request.GET['token'] if 'token' in self.request.GET else self.request.user.auth_token.key
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return HttpResponse(render_page('login', {'error': u'Неверный токен пользователя'}))

        session = create_new_session(user)

        response = HttpResponseRedirect(back_url)
        max_age = 30 * 24 * 60 * 60 # two weeks
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie('x-token', token, max_age=max_age, expires=expires)
        response.set_cookie('x-session', session.key, max_age=max_age, expires=expires)
        response.delete_cookie('sessionid')

        return response


class UserView(View):
    def get(self, *args, **kwargs):
        try:
            user_id = self.kwargs['user_id']
        except KeyError:
            return HttpResponseBadRequest()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        try:
            uvb = vbUser(user, extend=True, genres=True, friends=True)
            days = (timezone.now() - uvb.data['regdate']).days
            how_long = numeral.get_plural(days, (u'день', u'дня', u'дней'))

            default_user = uvb.data
            default_user.update({
                'regdate': uvb.data['regdate'].strftime("%Y-%m-%d"),
                'how_long': how_long
            })

            films = Films.objects.filter(uf_films_rel__user=user, uf_films_rel__subscribed=APP_USERFILM_SUBS_TRUE)
            films = Paginator(films, APP_USERS_API_DEFAULT_PER_PAGE).page(APP_USERS_API_DEFAULT_PAGE)
            vbf = vbFilm(films.object_list, many=True)

            actors = Persons.objects.filter(up_persons_rel__user=user, pf_persons_rel__p_type=APP_PERSON_ACTOR).distinct('id')
            actors = Paginator(actors, APP_USERS_API_DEFAULT_PER_PAGE).page(APP_USERS_API_DEFAULT_PAGE)
            vba = vbPerson(actors.object_list, many=True)

            directors = Persons.objects.filter(up_persons_rel__user=user, pf_persons_rel__p_type=APP_PERSON_DIRECTOR).distinct()
            directors = Paginator(directors, APP_USERS_API_DEFAULT_PER_PAGE).page(APP_USERS_API_DEFAULT_PAGE)
            vbd = vbPerson(directors.object_list, many=True)

            # Сериализуем
            o_feed = vbFeedElement(calc_feed(user.id), many=True).data

            default_user.update({
                'films': vbf.data,
                'actors': vba.data,
                'feed': o_feed,
                'directors': vbd.data,
            })

            return HttpResponse(render_page('user', {'user': default_user}))

        except Exception as e:
            return HttpResponseServerError(e)


class RestorePasswordView(View):

    def get(self, *args, **kwargs):
        return HttpResponse(render_page('restore_password', {}))

    def post(self, *args, **kwargs):
        if 'to' in self.request.POST:
            to = self.request.POST['to']
        else:
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(username=to)
            password = User.objects.make_random_password()
            user.set_password(password)
            kw = dict(subject=APP_SUBJECT_TO_RESTORE_PASSWORD,
                      tpl_name='restore_password_email.html',
                      context={'password': password},
                      to=[user.email])
            send_template_mail.apply_async(kwargs=kw)
        except User.DoesNotExist as e:
            return HttpResponseBadRequest(e)
        except Exception as e:
            return HttpResponseBadRequest(e)

        return redirect('login_view')


class UserProfileView(View):

    def get(self, request, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect("login_view")
        resp_dict = {'user': vbUserProfile(request.user.profile).data,
                     'error': request.GET.get('e', None)}
        return HttpResponse(render_page('profile', resp_dict))

    def post(self, request, **kwargs):
        uprofile_form = UsersProfileForm(data=request.POST, instance=request.user)
        if uprofile_form.is_valid():
            try:
                uprofile_form.save()
            except Exception as e:
                return HttpResponse(render_page('profile', {'error': e}))
        return redirect('profile_view')


def delete_social_provider(request, provider):
    if isinstance(request.user, AnonymousUser):
        return redirect("login_view")
    try:
        users_social = UserSocialAuth.objects.filter(user=request.user)
        if request.user.has_usable_password() or users_social.count() > 1:
            users_social.get(provider=provider).delete()
        else:
            kw = {'e': u'Невозможно удалить аккаунт социальной сети'.encode('utf-8')}
            url = url_with_querystring(reverse('profile_view'), **kw)
            return redirect(url)
    except:
        pass
    return redirect('profile_view')


def calc_feed(user_id):
    # Список подписок на фильм
    uf = UsersFilms.get_subscribed_films_by_user(user_id, flat=True)

    # Список подписок на персону
    up = UsersPersons.get_subscribed_persons_by_user(user_id, flat=True)

    # Выборка фидов
    o_feed = Feed.get_feeds_by_user(user_id, uf=uf, up=up)

    return o_feed


class FeedView(View):

    def get(self, **kwargs):
        if self.request.user.is_authenticated():
            # Сериализуем
            try:
                o_feed = vbFeedElement(calc_feed(self.request.user.id), many=True).data
            except Exception, e:
                raise Http404

            return HttpResponse(render_page('feed', {'feed': o_feed}))
        return redirect('login_view')
