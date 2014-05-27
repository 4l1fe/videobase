# coding: utf-8
from django import forms

from .models import User, UsersProfile


class UsersProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        kwargs['instance'] = self.user.profile
        super(UsersProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.user.username or self.user.email

    def save(self, commit=True):
        super(UsersProfileForm, self).save(commit)
        self.user.username = self.user.email = self.cleaned_data['email']
        self.user.save()

    class Meta:
        model = UsersProfile
        exclude = ('userpic_id', 'userpic_type', 'last_visited', 'user')


class CustomRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    is_active = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

    def __init__(self, **kwargs):
        super(CustomRegisterForm, self).__init__(**kwargs)
        self.fields['username'].required = False

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['email']
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValueError("Passwords not coincidence")
        else:
            return super(CustomRegisterForm, self).clean()

    def save(self, commit=True):
        instance = super(CustomRegisterForm, self).save(commit)
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active')


class UserUpdateForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)