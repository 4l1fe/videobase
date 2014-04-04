# coding: utf-8

from django.forms import ModelForm

from .models import Users


class CustomRegisterForm(ModelForm):

    class Meta:
        model = Users
        fields = ['email', 'password', 'fio']