# coding: utf-8

from django import forms

from .models import User, UsersProfile


class CustomRegisterForm(forms.ModelForm):
    real_username = forms.CharField(label='Имя', max_length=128, required=False)

    def __init__(self, **kwargs):
        super(CustomRegisterForm, self).__init__(**kwargs)
        self.fields['username'].required = False

    def clean(self):
        self.cleaned_data['username'] = self.cleaned_data['email']
        return super(CustomRegisterForm, self).clean()

    def save(self, commit=True):
        instance = super(CustomRegisterForm, self).save(commit)
        username = self.cleaned_data.get('real_username', None)
        if username is not None:
            UsersProfile.objects.create(username=username, user=instance)
        return instance

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.HiddenInput(),
        }
