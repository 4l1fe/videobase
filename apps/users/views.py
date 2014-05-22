# coding: utf-8

from pytils import numeral

from django.db import transaction
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, HttpResponseServerError, Http404
from django.middleware.csrf import CSRF_KEY_LENGTH
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.forms import AuthenticationForm
from tasks import send_template_mail

from rest_framework.authtoken.models import Token

from apps.users.models import Feed
from apps.users.api.serializers import vbUser, vbFeedElement
from apps.users.forms import CustomRegisterForm
from apps.users.api.utils import create_new_session
from apps.users.constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE,\
    APP_SUBJECT_TO_CONFIRM_REGISTER, APP_SUBJECT_TO_RESTORE_PASSWORD

from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_ACTOR, \
    APP_FILM_FULL_FILM, APP_FILM_SERIAL, APP_USERFILM_STATUS_SUBS, \
    APP_PERSONFILM_SUBS_TRUE, APP_USERFILM_SUBS_TRUE
from apps.films.api.serializers import vbFilm, vbPerson

from utils.common import url_with_querystring
from utils.noderender import render_page


class RegisterUserView(View):

    def get(self, *args, **kwargs):
        csrf_token = get_random_string(CSRF_KEY_LENGTH)
        resp_dict = {'csrf_token': csrf_token}
        response = HttpResponse(render_page('register', resp_dict))
        response.set_cookie("csrftoken", csrf_token)
        return response

    @transaction.commit_manually
    def post(self, *args, **kwargs):
        register_form = CustomRegisterForm(data=self.request.POST)
        if register_form.is_valid():
            user = register_form.save()
            kw = {'token': user.auth_token.key,
                  '_': timezone.now().date().strftime("%H%M%S")}
            url = url_with_querystring(reverse('tokenize'), **kw)
            url = "http://{host}{url}".format(host=self.request.get_host(), url=url)
            context = {'user': user, 'redirect_url': url}

            try:
                kw = dict(subject=APP_SUBJECT_TO_CONFIRM_REGISTER,
                          tpl_name='confirmation_register.html',
                          context=context,
                          to=[user.email])
                send_template_mail.apply_async(kwargs=kw)
            except Exception as e:
                transaction.rollback()
                return HttpResponseBadRequest

            transaction.commit()
            return redirect('index_view')

        else:
            transaction.rollback()
            return HttpResponseBadRequest()


class LoginUserView(View):

    def get(self, *args, **kwargs):
        csrf_token = get_random_string(CSRF_KEY_LENGTH)
        resp_dict = {'csrf_token': csrf_token}
        response = HttpResponse(render_page('login', resp_dict))
        response.set_cookie("csrftoken", csrf_token)
        return response

    def post(self, *args, **kwargs):
        login_form = AuthenticationForm(data=self.request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if not user.is_active:
                return HttpResponse(render_page('login', {'error': {'password': 'True'}}))
            kw = {'token': user.auth_token.key,
                  '_': timezone.now().date().strftime("%H%M%S")}
            url = url_with_querystring(reverse('tokenize'), **kw)
            return HttpResponseRedirect(url)
        else:
            return HttpResponse(render_page('login', {'error': {'password': 'True'}}))


class TokenizeView(View):

    @never_cache
    def get(self, *args, **kwargs):
        context = RequestContext(self.request)
        response_dict = {
            'back_url': self.request.GET['back_url'] if 'back_url' in self.request.GET else '',
            'token': ''
        }

        if 'token' in self.request.GET:
            response_dict['token'] = self.request.GET['token']
        else:
            response_dict['token'] = self.request.user.auth_token.key

        try:
            user = Token.objects.get(key=response_dict['token']).user
            user.is_active = True
            user.save()
        except:
            return HttpResponseBadRequest()

        session = create_new_session(user)
        response_dict['session_key'] = session.token.key

        return render_to_response('tokenize.html', response_dict, context_instance=context)


class UserView(View):
    def get(self, *args, **kwargs):
        try:
            user_id = self.kwargs['user_id']
        except KeyError:
            return HttpResponseBadRequest()

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return HttpResponseBadRequest()

        try:
            uvb = vbUser(user, extend=True, genres=True, friends=True)
            days = (timezone.now() - uvb.data['regdate']).days
            how_long = numeral.get_plural(days, (u'день', u'дня', u'дней'))
            default_user = {'regdate': uvb.data['regdate'].strftime("%Y-%m-%d"),
                            'how_long': how_long}
            default_user.update(uvb.data)

            films = Films.objects.filter(users_films__user=user,
                                         type__in=(APP_FILM_SERIAL, APP_FILM_FULL_FILM),
                                         users_films__status=APP_USERFILM_STATUS_SUBS)
            page_films = Paginator(films, APP_USERS_API_DEFAULT_PER_PAGE).page(APP_USERS_API_DEFAULT_PAGE)
            vbf = vbFilm(page_films.object_list, many=True)

            actors = Persons.objects.filter(users_persons__user=user,
                                            person_film_rel__p_type=APP_PERSON_ACTOR)
            page_actors = Paginator(actors, APP_USERS_API_DEFAULT_PER_PAGE).\
                page(APP_USERS_API_DEFAULT_PAGE)
            vba = vbPerson(page_actors.object_list, many=True)

            directors = Persons.objects.filter(users_persons__user=user,
                                               person_film_rel__p_type=APP_PERSON_DIRECTOR)
            page_directors = Paginator(directors, APP_USERS_API_DEFAULT_PER_PAGE).\
                page(APP_USERS_API_DEFAULT_PAGE)
            vbd = vbPerson(page_directors.object_list, many=True)

            default = {'user': default_user,
                       'films_subscribed': vbf.data,
                       'actors_fav': vba.data,
                       'feed': [],
                       'directors_fav': vbd.data,
                       }

            return HttpResponse(render_page('user', default))

        except Exception as e:
            return HttpResponseServerError()


class RestorePasswordView(View):

    def get(self, *args, **kwargs):
        csrf_token = get_random_string(CSRF_KEY_LENGTH)
        resp_dict = {'csrf_token': csrf_token}
        response = HttpResponse(render_page('restore_password', resp_dict))
        response.set_cookie("csrftoken", csrf_token)
        return response

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

# TODO: DONT DELETE THIS COMMENTS!
# class ProfileEdit(TemplateView):
#     template_name = 'profile.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.user = request.user
#         return super(ProfileEdit, self).dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         user = self.request.user
#         uprofile_form = UsersProfileForm(user=user)
#         resp_dict = {
#         'uprofile_form': uprofile_form
#         }
#         resp_dict.update(csrf(self.request))
#         return resp_dict
#
#     def post(self, request, **kwargs):
#         uprofile_form = UsersProfileForm(data=request.POST, files=request.FILES,
#                                          user=self.user)
#         if uprofile_form.is_valid():
#             try:
#                 uprofile_form.save()
#             except Exception as e:
#                 print e
#         return HttpResponseRedirect('/users/profile/')


def feed_view(request):
    if request.user.is_authenticated():
        user_id = request.user.id

        # Список подписок на фильм
        uf = UsersFilms.get_subscribed_films_by_user(user_id, flat=True)

        # Список подписок на персону
        up = UsersPersons.get_subscribed_persons_by_user(user_id, flat=True)

        # Выборка фидов
        o_feed = Feed.get_feeds_by_user(user_id, uf=uf, up=up)

        # Сериализуем
        try:
            o_feed = vbFeedElement(o_feed, many=True).data
        except Exception, e:
            raise Http404

        return HttpResponse(render_page('feed', {'feed': o_feed}))

    return redirect('login_view')
