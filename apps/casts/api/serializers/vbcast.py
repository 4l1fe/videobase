# coding: utf-8

from rest_framework import serializers

from apps.casts.models import Casts, UsersCasts

class vbCast(serializers.ModelSerializer):

    tags = serializers.SerializerMethodField('tags_list')
    locations = serializers.SerializerMethodField('locations_list')
    relation = serializers.SerializerMethodField('calc_relation')

    def tags_list(self, obj):
        return [{
            'id': tag.type,
            'name': tag.name,
            'type': tag.type
        } for tag in obj.tags]

    def locations_list(self, obj):
        return [{
            'id': l.id,
            'service': l.cast_service.id,
            'quality': l.quality,
            'price_type': l.price_type,
            'price': l.price,
            'url_view': l.url_view,
            'value': l.value
        } for l in obj.cl_location_rel]

    def relation_calc(self, obj):
        return {}

    class Meta:
        model = Casts
        fields = (
            'id', 'title', 'title_orig', 'description', 'status', 'pg_rating',
            'start', 'duration',
#            'tags', 'poster', 'locations', 'relation'
        )
