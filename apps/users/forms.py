# coding: utf-8

from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.db import transaction, IntegrityError

from videobase.settings import HOST

from apps.users.tasks import send_template_mail
from apps.users.models import User, UsersProfile, UsersHash
from apps.users.constants import APP_SUBJECT_TO_RESTORE_EMAIL, APP_USER_ACTIVE_KEY, \
    APP_SUBJECT_TO_CONFIRM_REGISTER, APP_USER_HASH_EMAIL, APP_USER_HASH_REGISTR

from utils.common import url_with_querystring


class UsersProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=True, max_length=30)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        kwargs['instance'] = self.user.profile

        super(UsersProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.user.email


    @transaction.commit_manually
    def save(self, commit=True, send_email=False):
        try:
            email = self.cleaned_data['email']
            email_flag = True if self.user.username != email or self.user.email != email else False

            if email_flag:
                # Save confirm email
                self.instance.deactivation_email()

                # Save hash
                o_hash = UsersHash(user=self.user, hash_type=APP_USER_HASH_EMAIL)
                o_hash.save()

            instance = super(UsersProfileForm, self).save(commit=False)
        except IntegrityError, e:
            transaction.rollback()
            return {'error': e.message}

        if email_flag:
            try:
                # Save email
                self.user.email = email
                self.user.username = email

                self.user.save()
            except Exception, e:
                transaction.rollback()
                return {'email': "Ошибка в сохранении email"}

        try:
            self.user.first_name = self.cleaned_data['username']
            self.user.save()
        except IntegrityError, e:
            transaction.rollback()
            return {'username': "Ошибка в сохранении имени"}

        try:
            transaction.commit()
        except IntegrityError, e:
            transaction.rollback()
            return {'error': "Ошибка в сохранении имени"}

        if send_email and email_flag:
            # Формируем параметры email
            param_email = {
                'to': [email],
                'context': {
                    'user': model_to_dict(self.user, fields=[field.name for field in self.user._meta.fields]),
                    'profile': model_to_dict(instance, fields=[field.name for field in instance._meta.fields]),
                    'url': 'http://{host}{url}'.format(
                        host=HOST,
                        url=url_with_querystring(reverse('confirm_email'), **{APP_USER_ACTIVE_KEY: o_hash.hash_key})
                    ),
                },
                'subject': APP_SUBJECT_TO_RESTORE_EMAIL,
                'tpl_name': 'confirm_change_email.html',
            }

            # Отправляем email
            send_template_mail.apply_async(kwargs=param_email)

        return instance


    class Meta:
        model = UsersProfile
        exclude = ('userpic_id', 'userpic_type', 'last_visited', 'user')


class CustomRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)

    error_messages = {
        'passwords_not_equal': u'Пароли не совпадают',
        'email': u'Email-обязательное поле!',
    }

    def __init__(self, **kwargs):
        super(CustomRegisterForm, self).__init__(**kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = True


    def clean(self):
        if 'email' in self.cleaned_data:
            self.cleaned_data['username'] = self.cleaned_data.get('email')
        else:
            raise forms.ValidationError(self.error_messages['email'], code='email')

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(self.error_messages['passwords_not_equal'],
                                            code='password_not_equal')
            else:
                return super(CustomRegisterForm, self).clean()
        else:
            raise forms.ValidationError('Password is required field')


    @transaction.commit_on_success
    def save(self, commit=True, send_email=False):
        instance = super(CustomRegisterForm, self).save(commit)
        instance.first_name = self.cleaned_data['email'].split('@')[0]
        instance.set_password(self.cleaned_data['password1'])
        instance.save()

        # save hash
        o_hash = UsersHash(user=instance.user, hash_type=APP_USER_HASH_REGISTR)
        o_hash.save()

        if send_email:
            param_email = {
                'to': [instance.email],
                'context': {
                    'user': model_to_dict(instance, fields=[field.name for field in instance._meta.fields]),
                    'redirect_url': 'http://{host}{url}'.format(
                        host=HOST,
                        url=url_with_querystring(reverse('confirm_email'), **{APP_USER_ACTIVE_KEY: o_hash.hash_key})
                    )
                },
                'subject': APP_SUBJECT_TO_CONFIRM_REGISTER,
                'tpl_name': 'confirmation_register.html',
            }

            send_template_mail.apply_async(kwargs=param_email)

        return instance


    class Meta:
        model = User
        fields = ('email', 'username')


class UserUpdateForm(forms.Form):
    name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
