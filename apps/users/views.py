# coding: utf-8
import datetime
from pytils import numeral
from django.db import transaction
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, HttpResponse, HttpResponseForbidden,
                         HttpResponseBadRequest, HttpResponseServerError, Http404)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.views import SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, AnonymousUser
from social.apps.django_app.default.models import UserSocialAuth
from rest_framework.authtoken.models import Token
from videobase.settings import HOST
from apps.users.models import Feed, SessionToken, UsersHash
from apps.users.tasks import send_template_mail
from apps.users.api.serializers import vbUser, vbFeedElement, vbUserProfile
from apps.users.forms import CustomRegisterForm, UsersProfileForm
from apps.users.api.utils import create_new_session
from apps.users.constants import (APP_USERS_API_DEFAULT_PAGE, APP_USERS_API_DEFAULT_PER_PAGE,
                                  APP_SUBJECT_TO_RESTORE_PASSWORD, APP_USER_ACTIVE_KEY, APP_USER_HASH_EMAIL,
                                  APP_USER_HASH_REGISTR, APP_USER_HASH_PASSWD, APP_USER_PIC_TYPE_LOCAL)
from apps.films.models import Films, Persons, UsersFilms, UsersPersons
from apps.films.constants import APP_PERSON_DIRECTOR, APP_PERSON_ACTOR, APP_USERFILM_SUBS_TRUE
from apps.films.api.serializers import vbFilm, vbPerson
from utils.common import url_with_querystring
from utils.noderender import render_page
from apps.users import UsersPics


class RegisterUserView(View):

    def get(self, *args, **kwargs):
        return HttpResponse(render_page('register', {}))

    @transaction.commit_manually
    def post(self, *args, **kwargs):
        register_form = CustomRegisterForm(data=self.request.POST)
        if register_form.is_valid():
            committed = False
            try:
                user = register_form.save(send_email=True)
                url_redirect = url_with_querystring(
                    reverse('tokenize'),
                    **{
                        'token': user.auth_token.key,
                        '_': timezone.now().date().strftime("%H%M%S"),
                    }
                )
                transaction.commit()
                committed = True

                return redirect(url_redirect)

            except Exception, e:
                resp_dict = {'error': 'Ошибка в сохранении данных.'}
                return HttpResponse(render_page('register', resp_dict))

            finally:
                if not committed:
                    transaction.rollback()

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
        data = self.request.POST
        login_form = AuthenticationForm(data=data)
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
        x_session = request.COOKIES.get('x-session')
        try:
            session = SessionToken.objects.get(key=x_session)
            session.is_active = False
            session.save()
        except Exception, e:
            pass
        
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

        # 30 days in the seconds
        max_age = 30 * 86400

        # Set expires
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
        expires = datetime.datetime.strftime(expires, "%a, %d-%b-%Y %H:%M:%S GMT")

        # Set Response
        response = HttpResponseRedirect(back_url)
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


class ConfirmEmailView(View):

    def get(self, request, *args, **kwargs):
        key = request.GET.get(APP_USER_ACTIVE_KEY, None)
        if key is None:
            raise Http404

        user_hash = UsersHash.get_by_hash(hash_key=key, hash_type=[APP_USER_HASH_EMAIL, APP_USER_HASH_REGISTR])
        if user_hash is None:
            raise Http404

        profile = user_hash.user.profile
        profile.confirm_email = True
        profile.save()

        return HttpResponse(render_page('confirm_email', {}))


class ResetPasswordView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse(render_page('reset_passwd', {}))

        raise Http404

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', False)

            active_users = User.objects.filter(username__iexact=email, email__isnull=False, is_active=True)
            for user in active_users:
                # Save hash
                o_hash = UsersHash(user=user, hash_type=APP_USER_HASH_PASSWD)
                o_hash.save()

                # Формируем параметры email
                param_email = {
                    'to': [user.email],
                    'context': {
                        'url': 'http://{host}{url}'.format(
                            host=HOST,
                            url=reverse('reset_pwd', args=(urlsafe_base64_encode(str(user.id)), o_hash.hash_key)),
                        ),
                        'user': model_to_dict(user, fields=[field.name for field in user._meta.fields]),
                    },
                    'subject': APP_SUBJECT_TO_RESTORE_PASSWORD,
                    'tpl_name': 'mail/password_email_restore.html',
                }

                # Отправляем email
                send_template_mail.apply_async(kwargs=param_email)

            return HttpResponseRedirect(reverse('reset_done'))

        else:
             HttpResponse(render_page('reset_passwd', {'error': u'Введите корректный email'}))


class UserProfileView(View):

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        resp_dict = {
            'user': vbUserProfile(request.user.profile).data,
            'error': request.GET.get('e', None)
        }

        return HttpResponse(render_page('profile', resp_dict))

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = UsersProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False, send_email=True)
            image = form.cleaned_data['avatar']

            if isinstance(profile, dict):
                t = vbUserProfile(request.user.profile).data
                t.update(request.POST.dict())
                return HttpResponse(render_page('profile', {'user': t, 'error': profile}))
            
            if image:
                up = UsersPics.objects.create(user=request.user, type=APP_USER_PIC_TYPE_LOCAL)
                up.image = image  # чтобы в имени был id
                up.save()
                profile.userpic_id = up.pk
            profile.save()

            return HttpResponse(render_page('profile', {'user': vbUserProfile(profile).data}))

        return redirect('profile_view')


class ConfirmResetPwdView(View):

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return user


    def check_user_and_token(self, user, token):
        user_hash = UsersHash.get_by_hash(hash_key=token, hash_type=[APP_USER_HASH_PASSWD])
        return True if not (user is None or user_hash is None) and user.id == user_hash.user.id else False


    def get(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(uidb64)
        if self.check_user_and_token(user, token):
            return HttpResponse(render_page('confirm_passwd', {}))

        return HttpResponse(render_page('confirm_passwd', {'error': {'token': True}}))


    def post(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(uidb64)
        if self.check_user_and_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()

                if len(user.email):
                    # Формируем параметры email
                    param_email = {
                        'to': [user.email],
                        'context': {
                            'user': model_to_dict(user, fields=[field.name for field in user._meta.fields]),
                        },
                        'subject': APP_SUBJECT_TO_RESTORE_PASSWORD,
                        'tpl_name': 'mail/password_email_confirm.html',
                    }

                    # Отправляем email
                    send_template_mail.apply_async(kwargs=param_email)

                return HttpResponseRedirect(reverse('reset_confirm'))

            else:
                return HttpResponse(render_page('confirm_passwd', {'error': dict(((i[0], i[1][0]) for i in form.errors.items()))}))

        return HttpResponse(render_page('confirm_passwd', {'error': {'token': True}}))


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
    except Exception, e:
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

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            # Сериализуем
            try:
                o_feed = vbFeedElement(calc_feed(self.request.user.id), many=True).data
            except Exception, e:
                raise Http404

            return HttpResponse(render_page('feed', {'feed': o_feed}))

        return redirect('login_view')


def password_reset_done(request):
    return HttpResponse(render_page('reset_passwd', {'send': True}))


def password_reset_confirm(request):
    return HttpResponse(render_page('confirm_passwd', {'confirm': True}))
