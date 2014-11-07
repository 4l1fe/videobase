# coding: utf-8

from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.films.constants import APP_FILM_PERSON_TYPES
from apps.films.models import Persons, PersonsFilms, UsersPersons


#############################################################################################################
#
class vbPerson(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField('get_path_to_photo')
    birthplace = serializers.SerializerMethodField('get_birthplace')
    relation = serializers.SerializerMethodField('get_relation')
    roles = serializers.SerializerMethodField('get_roles')

    def __init__(self, *args, **kwargs):  # TODO: подготовить список городов, стран для получения места рождения
        extended_fields = []

        extend = kwargs.pop('extend', False)
        self.user = kwargs.pop('user', False)
        if not extend:
            extended_fields += ['bio', 'roles']

        # Instantiate the superclass normally
        super(vbPerson, self).__init__(*args, **kwargs)

        if extended_fields:
            # Drop keys if they exist
            for field_name in extended_fields:
                self.fields.pop(field_name, None)

        if not self.user:
            self.fields.pop('relation', None)

        self.prep_person_list = self._get_person_list()
        self.prep_person_roles = self._get_roles()

    def _get_person_list(self):
        persons_list = []
        if self.object:
            if not hasattr(self.object, '__iter__'):  # если вдруг один экземпляр.
                persons_list.append(self.object)
            else:
                return self.object
        return persons_list

    def _get_roles(self):
        """
        Подготовим словарь из ролей, под которыми человек принимал участие в фильме.
        Далее будем использовать его для того, чтобы уже выбирать роли только по отдельному человеку.
        """

        person_roles = PersonsFilms.objects.\
            filter(person__in=self.prep_person_list).\
            distinct('person', 'p_type').\
            values_list('person', 'p_type')

        prep_person_roles = defaultdict(list)
        for p,r in person_roles:
            prep_person_roles[p].append(r)

        return prep_person_roles

    def get_path_to_photo(self, obj):
        return obj.get_path_to_photo

    def get_relation(self, obj):
        if self.user:
            try:
                up = UsersPersons.objects.get(person=obj, user=self.user)
                return up.subscribed
            except ObjectDoesNotExist:
                return 0  # должен быть тип поля UsersPersons.subscribed

    def get_birthplace(self, obj):
        if obj.city is not None:
            city = obj.city
            return [city.name, city.country.name]

        return []

    def get_roles(self, obj):
        roles_display = []
        if obj.pk in self.prep_person_roles:
            d = dict(APP_FILM_PERSON_TYPES)
            for role in self.prep_person_roles[obj.pk]:
                roles_display.append(d[role])

        return roles_display

    class Meta:
        model = Persons
        fields = [
            'id', 'name', 'name_orig', 'photo', 'relation',
            'birthdate', 'birthplace', 'bio', 'roles'
        ]
