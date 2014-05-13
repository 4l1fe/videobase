# coding: utf-8


from django.forms import ModelForm
from .models import UsersProfile, UsersPics
from django.contrib.auth.models import User
from django import forms
from .models import User, UsersProfile


class UsersProfileForm(forms.Form):
    nickname  = forms.CharField(label=u'Имя пользователя', max_length=128, required=False)
    email     = forms.EmailField(label=u'Email', required=False)
    phone     = forms.CharField(label=u'Телефон', max_length=13, required=False)
    image     = forms.ImageField(label=u'Аватарка', required=False)

    def __init__(self, user, **kwargs):
        super(UsersProfileForm, self).__init__(**kwargs)
        self.user = user
        self.profile = user.profile
        self.fields['nickname'].initial = user.profile.nickname
        self.fields['email'].initial = user.email
        self.fields['phone'].initial = user.profile.phone
        try:
            default = UsersPics.objects.get(pk=user.profile.userpic_id)
        except UsersPics.DoesNotExist:
            default = None
        kwargs = {}
        if default:
            kwargs['empty_label'] = default
        self.fields['user_pic'] = forms.ModelChoiceField(queryset=user.pics.all(), label=u'Выбор аватарки', required=False, **kwargs)

    def save(self):
        self.profile.phone = self.cleaned_data['phone']
        self.profile.nickname = self.cleaned_data['nickname']
        self.user.email = self.user.username = self.cleaned_data['email']
        if self.cleaned_data['image']:
            pic = UsersPics(user=self.user, image=self.cleaned_data['image'])
            pic.save()
        if self.cleaned_data['user_pic']:
            self.profile.userpic_id = self.cleaned_data['user_pic'].pk

        self.profile.save()
        self.user.save()


class CustomRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

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
        fields = ('email', 'password', 'username', )


class UserUpdateForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)