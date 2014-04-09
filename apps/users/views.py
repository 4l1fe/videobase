# coding: utf-8
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from constants import SUBJECT_TO_RESTORE_PASSWORD
from .forms import UsersProfileForm, CustomRegisterForm


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
        uprofile_form = UsersProfileForm(data=request.POST, files=request.FILES, user=self.user)
        if uprofile_form.is_valid():
            try:
                uprofile_form.save()
            except Exception as e:
                print e
        return HttpResponseRedirect('/users/profile/')


class RegisterUserView(CreateView):
    template_name = 'register.html'
    form_class = CustomRegisterForm
    success_url = '/'


def restore_password(request):
    response = HttpResponse(status=200)
    if request.method == 'POST' and 'to' in request.POST:
        to = request.POST['to']
        try:
            user = User.objects.get(username=to)
            password = User.objects.make_random_password()
            user.set_password(password)
            tpl = render_to_string('restore_password.html',
                                   {'password': password})
            msg = EmailMultiAlternatives(subject=SUBJECT_TO_RESTORE_PASSWORD, to=[to])
            msg.attach_alternative(tpl, 'text/html')
        except User.DoesNotExist:
            response = HttpResponseBadRequest()
    else:
        response = HttpResponseBadRequest()

    return response


