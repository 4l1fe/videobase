# coding: utf-8
from django.core.context_processors import csrf
from django.middleware.csrf import CSRF_KEY_LENGTH
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import AuthenticationForm

from constants import SUBJECT_TO_RESTORE_PASSWORD
from apps.users.api.utils import create_new_session
from .forms import UsersProfileForm, CustomRegisterForm

from utils.noderender import render_page


class ProfileEdit(TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(ProfileEdit, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        uprofile_form = UsersProfileForm(user=user)
        resp_dict = {
        'uprofile_form': uprofile_form
        }
        resp_dict.update(csrf(self.request))
        return resp_dict

    def post(self, request, **kwargs):
        uprofile_form = UsersProfileForm(data=request.POST, files=request.FILES,
                                         user=self.user)
        if uprofile_form.is_valid():
            try:
                uprofile_form.save()
            except Exception as e:
                print e
        return HttpResponseRedirect('/users/profile/')


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
            register_form.save()
        return HttpResponseRedirect("/")


class LoginUserView(View):

    def get(self, *args, **kwargs):
        csrf_token = get_random_string(CSRF_KEY_LENGTH)
        resp_dict = {'csrf_token': csrf_token}
        response = HttpResponse(render_page('login', resp_dict))
        response.set_cookie("csrftoken", csrf_token)
        return response


def restore_password(request):
    resp_dict = {}
    resp_dict.update(csrf(request))
    response = render_to_response('restore_password_form.html',)
    if request.method == 'POST' and 'to' in request.POST:
        to = request.POST['to']
        try:
            user = User.objects.get(username=to)
            password = User.objects.make_random_password()
            user.set_password(password)
            tpl = render_to_string('restore_password_email.html',
                                   {'password': password})
            msg = EmailMultiAlternatives(subject=SUBJECT_TO_RESTORE_PASSWORD, to=[to])
            msg.attach_alternative(tpl, 'text/html')
        except User.DoesNotExist as e:
            response = HttpResponseBadRequest(e)
        except Exception as e:
            response = HttpResponseBadRequest(e)

    return response
