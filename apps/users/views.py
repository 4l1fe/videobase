# coding: utf-8

from django.views.generic import CreateView
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.template.loader import render_to_string


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
            msg.send(fail_silently=True)
        except User.DoesNotExist as e:
            response = HttpResponseBadRequest(e)
        except Exception as e:
            response = HttpResponseBadRequest(e)
    else:
        response = HttpResponseBadRequest()

    return response