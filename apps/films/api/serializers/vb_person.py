# coding: utf-8

from rest_framework import serializers
from apps.films.models import Persons, PersonsFilms


#############################################################################################################
#
class vbPerson(serializers.ModelSerializer):
    birthplace = serializers.SerializerMethodField('get_birthplace')
    relation = serializers.SerializerMethodField('get_relation')
    roles = serializers.SerializerMethodField('get_roles')

    def __init__(self, *args, **kwargs):  # TODO: подготовить список городов, стран для получения места рождения
                                          # TODO: подготовить список ролей, для получения их по каждой персоне
        extended_fields = []

        extend = kwargs.pop('extend', False)
        if not extend:
            extended_fields += ['bio', 'roles']

        # Instantiate the superclass normally
        super(vbPerson, self).__init__(*args, **kwargs)

        if len(extended_fields):
            # Drop keys if they exist
            for field_name in extended_fields:
                self.fields.pop(field_name, None)

        self.prepared_roles = self._get_roles()

    def get_relation(self, obj):
        pass

    def get_birthplace(self, obj):
        if not obj.city is None:
            city = obj.city.name
            country = obj.city.country.name
            return [city, country]
        return []

    def _get_roles(self):
        persons_list = self.object
        person_roles = PersonsFilms.objects.filter(person__in=persons_list).distinct('person', 'p_type')

    def get_roles(self, obj):
        if obj.person_film_rel is not None:
            return (pf.p_type for pf in obj.person_film_rel.distinct('p_type'))
        return []

    class Meta:
        model = Persons
        fields = ('id', 'name', 'photo', 'relation', 'birthdate', 'birthplace', 'bio', 'roles')
