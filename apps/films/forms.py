# coding: utf-8

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.films.models import *


#############################################################################################################
# Форома для заполнения сезона в админке
class SeasonsAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(SeasonsAdminForm, self).clean()

        if cleaned_data and not self._errors:
            if cleaned_data['film'].ftype != SERIAL:
                raise ValidationError(u'У фильма не может быть сезона')

        return cleaned_data


    class Meta:
        model = Seasons
