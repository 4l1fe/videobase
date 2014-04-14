# coding: utf-8
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import UsersProfileEditForm, UserEditForm
from apps.users.models import UsersProfile
from apps.users.api.utils import create_new_session
from apps.users.forms import UserPicsEditForm


def profile_edit(request):
    if request.method == 'POST':  # If the form has been submitted...
        # ContactForm was defined in the the previous section

        up_form = UsersProfileEditForm(request.POST)  #A form bound to the POST data
        u_form = UserEditForm(request.POST)

        if up_form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            up_form.save()
        if u_form.is_valid():
            form2.save()
        upics_form = UserPicsEditForm(request.POST, request.FILES)
        if upics_form.is_valid():
            upics_form.save()
            return HttpResponseRedirect('/profile/')  # Redirect after POST

    else:

        uprofile = UsersProfile.objects.get(user=request.user)
        upic = UsersProfile.objects.get(user=request.user)
        uprofile_form = UsersProfileEditForm(instance=uprofile)
        user_email_form = UserEditForm(instance=request.user)
        user_pics_form = UserPicsEditForm(instance=upic)

    c = {
        'uprofile_form': uprofile_form,
        'user_email_form': user_email_form,
        'form3': user_pics_form,
    }
    c.update(csrf(request))
    #return HttpResponseRedirect('/admin/')
    return render_to_response('profile.html', c)


from .forms import CustomRegisterForm
from constants import SUBJECT_TO_RESTORE_PASSWORD


class RegisterUserView(CreateView):
    template_name = 'register.html'
    form_class = CustomRegisterForm
    success_url = '/'


def restore_password(request):
    response = None
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


class ObtainSessionToken(APIView):
    def get(self, request, format=None, resource_id=None, extend=False):

        #try:
        if True:
            session = create_new_session(request.user)

            print(session.created)
            response_dict = {'session': session.pk,
                             'expires': session.get_expiration_time(),
                             'session_token': session.token.key

            }
        try:
            pass
        except Exception, e:
            print e
            raise Http404
            # Any URL parameters get passed in **kw

        response = Response(response_dict, status=status.HTTP_200_OK)
        return response


