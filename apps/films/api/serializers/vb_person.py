# coding: utf-8

from rest_framework import serializers
from apps.films.models import Persons


#############################################################################################################
#
class vbPerson(serializers.ModelSerializer):
    birthplace = serializers.SerializerMethodField('get_birthplace')

    def __init__(self, *args, **kwargs):
        new_fields = []

        extend = kwargs.pop('extend', False)
        if not extend:
            new_fields += ['bio']

        # Instantiate the superclass normally
        super(vbPerson, self).__init__(*args, **kwargs)

        if len(new_fields):
            # Drop keys if they exist
            for field_name in new_fields:
                self.fields.pop(field_name, None)

    def get_birthplace(self, obj):
        city = obj.city_id.name
        country = obj.city_id.country_id.name
        return (city, country)

    class Meta:
        model = Persons
        fields = ('id', 'name', 'photo', 'bio', 'birthplace')
