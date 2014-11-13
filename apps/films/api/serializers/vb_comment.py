# coding: utf-8

from rest_framework import serializers
from apps.contents.models import Comments
from apps.users.models import UsersPics
import pytz
from videobase.settings import TIME_ZONE


################################################################################
class vbComment(serializers.ModelSerializer):
    film = serializers.SerializerMethodField('calc_film')
    user = serializers.SerializerMethodField('calc_user')
    created = serializers.SerializerMethodField('calc_created')

    def calc_film(self, obj):
        film = obj.content.film
        return {
            'id': film.id,
            'name': film.name,
        }


    def calc_created(self, obj):
        return pytz.timezone(TIME_ZONE).localize(obj.created, is_dst=None)


    def calc_user(self, obj):
        path = ''
        user = obj.user
        profile = user.profile
        userpic = profile.userpic_id

        try:
            image = UsersPics.objects.get(id=userpic).image
            path = image.storage.url(image.name)
        except:
            pass

        return {
            'id': user.id,
            'name': profile.get_name(),
            'avatar': path,
        }

    class Meta:
        model = Comments
        fields = ('id', 'film', 'user', 'text', 'created',)
