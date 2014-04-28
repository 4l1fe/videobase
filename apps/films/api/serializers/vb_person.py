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

        self.prep_person_roles = self._get_roles()

    def _get_roles(self):
        """Подготовим словарь из ролей, под которыми человек принимал участие в фильме.
        Далее будем использовать его для того, чтобы уже выбирать роли только по отдельному человеку."""

        persons_list = self.object  # должен быть список из объектов - Persons
        person_roles = PersonsFilms.objects.filter(person__in=persons_list).\
                                            distinct('person', 'p_type').values_list('person', 'p_type')
        prep_person_roles = {}
        for p, r in person_roles.items():
            if p not in prep_person_roles:
                prep_person_roles[p] = [r]
            else:
                prep_person_roles[p].append(r)
        return prep_person_roles

    def get_relation(self, obj):
        return 'relation'

    def get_birthplace(self, obj):
        if not obj.city is None:
            city = obj.city.name
            country = obj.city.country.name
            return [city, country]
        return []

    def get_roles(self, obj):
        if obj.pk in self.prep_person_roles:
            return self.prep_person_roles[obj.pk]
        return []

    class Meta:
        model = Persons
        fields = ('id', 'name', 'photo', 'relation', 'birthdate', 'birthplace', 'bio', 'roles')
