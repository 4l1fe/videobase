# coding: utf-8

from rest_framework import serializers
import time
from apps.casts.models import Casts, UsersCasts

class vbCast(serializers.ModelSerializer):

    tags = serializers.SerializerMethodField('tags_list')
    locations = serializers.SerializerMethodField('locations_list')
    relation = serializers.SerializerMethodField('calc_relation')
    poster = serializers.SerializerMethodField('get_poster')
    start = serializers.SerializerMethodField('get_start')

    def tags_list(self, obj):
        return [{
            'id': tag.type,
            'name': tag.name,
            'type': tag.type
        } for tag in obj.tags.all()]

    def get_poster(self, obj):
        return obj.ce_cast_rel.first().get_photo_url() if obj.ce_cast_rel.first() else None

    def get_start(self, obj):
        return int(time.mktime(obj.start.utctimetuple()))

    def locations_list(self, obj):
        return [{
            'id': l.id,
            'type': l.cast_service.name,
            'quality': l.quality,
            'price_type': l.price_type,
            'price': l.price,
            'url_view': l.url_view,
            'value': l.value
        } for l in obj.cl_location_rel.all()]

    def relation_calc(self, obj):
        return {}

    class Meta:
        model = Casts
        fields = [
            'id', 'title', 'title_orig', 'description', 'status', 'pg_rating',
            'start', 'duration',
            'tags',
            'poster',
            'locations',
#           'relation'
        ]
