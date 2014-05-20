from rest_framework import serializers
from apps.users.models.users_feed import Feed
from .vb_user import vbUser


FEED_TYPE = {
    'film-r': {'id':'id',
               'name':'name',
               'rating':'rating'},
    'film-s': {'id':'id',
               'name':'name'},
    'film-nw': {'id':'id',
               'name':'name'},
    'film-c': {'id':'id',
               'text':'text',
               'film': {'id':'id',
                        'name':'name'}},
    'film-o': {'id':'id',
                'name':'name',
                'poster':'poster',
                'locations':{'id':'id',
                             'name':'name',
                             'price':'price',
                             'price_type':'price_type'}},
    'pers-s': {'id':'id',
                'name':'name',
                'photo':'photo'},
    'pers-o': {'id':'id',
                'name':'name',
                'photo':'photo',
                'type': 'type',
                'film': {'id':'id',
                        'name':'name'}},
    'user-a': {'id':'id',
                'name':'name',
                'avatar':'avatar'},
    'user-f': {'id':'id',
                'name':'name',
                'avatar':'avatar'},
    'sys-a': {}
}


class vbFeedElement(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_vbUser')

    def get_vbUser(self, obj):
        return vbUser(obj.user)

    class Meta:
        model = Feed
        fields = ('user', 'created', 'type', 'object', 'text')