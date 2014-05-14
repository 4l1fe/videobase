# coding: utf-8
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, HttpResponseServerError
from django.middleware.csrf import CSRF_KEY_LENGTH
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic import View, RedirectView
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.forms import AuthenticationForm

from constants import APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE
from .forms import CustomRegisterForm
from .api.serializers import vbUser
from apps.films.models import Films, Persons
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_ACTOR, \
    APP_FILM_FULL_FILM, APP_FILM_SERIAL, APP_USERFILM_STATUS_SUBS
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

    def post(self, *args, **kwargs):
        register_form = CustomRegisterForm(data=self.request.POST)
        if register_form.is_valid():
            user = register_form.save()
            kw = {'token': user.auth_token.key}
            url = url_with_querystring(reverse('tokenize'), **kw)
            return HttpResponseRedirect(url)
        else:
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
            kw = {'token': user.auth_token.key}
            url = url_with_querystring(reverse('tokenize'), **kw)
            return HttpResponseRedirect(url)
        else:
            return HttpResponseBadRequest()


class RedirectOAuthView(RedirectView):

    url = 'tokenize'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user:
            kw = {'token': self.request.user.auth_token.key}
            url = url_with_querystring(reverse(self.url), **kw)
        else:
            return None

        return url


class TokenizeView(View):

    def get(self, *args, **kwargs):
        context = RequestContext(self.request)
        response_dict = {}
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
            delta = timezone.now() - uvb.data['regdate']
            how_long = u"{}".format(delta.days if delta.days != 0 else 1)
            if delta.days % 10 in [0, 1]:
                day_title = u"день"
            elif delta.days % 10 in [2, 3, 4, ]:
                day_title = u"дня"
            else:
                day_title = u"дней"
            how_long += u" {}".format(day_title)
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
#
#
# def restore_password(request):
#     resp_dict = {}
#     resp_dict.update(csrf(request))
#     response = render_to_response('restore_password_form.html',)
#     if request.method == 'POST' and 'to' in request.POST:
#         to = request.POST['to']
#         try:
#             user = User.objects.get(username=to)
#             password = User.objects.make_random_password()
#             user.set_password(password)
#             tpl = render_to_string('restore_password_email.html',
#                                    {'password': password})
#             msg = EmailMultiAlternatives(subject=SUBJECT_TO_RESTORE_PASSWORD, to=[to])
#             msg.attach_alternative(tpl, 'text/html')
#         except User.DoesNotExist as e:
#             response = HttpResponseBadRequest(e)
#         except Exception as e:
#             response = HttpResponseBadRequest(e)
#
#     return response