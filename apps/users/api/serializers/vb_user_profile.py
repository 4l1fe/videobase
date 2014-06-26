# coding: utf-8
from rest_framework import serializers

from apps.users.models import UsersProfile


class vbUserProfile(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    email = serializers.SerializerMethodField('get_email')
    social = serializers.SerializerMethodField('get_social')

    def get_name(self, obj):
        return obj.get_name()

    def get_social(self, obj):
        resp_dict = {'facebook': False,
                     'twitter': False,
                     'vk': False,
                     'gplus': False}
        for social in obj.user.social_auth.all():
            if social.provider == 'vk-oauth':
                resp_dict['vk'] = True
            elif social.provider == 'google-oauth2':
                resp_dict['gplus'] = True
        return resp_dict

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = UsersProfile
        exclude = ('userpic_id', 'userpic_type', 'last_visited', 'user', 'id')