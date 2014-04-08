# coding: utf-8

from django.forms import ModelForm
from .models import UsersProfile, UsersPics
from django.contrib.auth.models import User

class UsersProfileEditForm(ModelForm):

    class Meta:
        model = UsersProfile
        fields = ['userpic_id',]

class UserEditForm(ModelForm):

    class Meta:
        model = User
        fields = ['email',]

class UserPicsEditForm(ModelForm):
    class Meta:
        model = UsersPics
        fields = ['url',]

    