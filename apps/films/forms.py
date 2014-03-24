# coding: utf-8

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.films.models import Persons,Seasons


#############################################################################################################
# Форома для заполнения сезона в админке
class SeasonsAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(SeasonsAdminForm, self).clean()

        if cleaned_data and not self._errors:
            if cleaned_data['film'].ftype != APP_FILM_SERIAL:
                raise ValidationError(u'У фильма не может быть сезона')

        return cleaned_data


    class Meta:
        model = Seasons

class PersonsImageForm(ModelForm):

    class Media:

        js = (#'/static/jcrop/js/jquery.min.js',
              'http://code.jquery.com/jquery-1.9.1.js',
            'http://cdnjs.cloudflare.com/ajax/libs/camanjs/3.3.0/caman.full.min.js',
            
            'http://code.jquery.com/ui/1.10.4/jquery-ui.js',
              '/static/jcrop/js/jquery.Jcrop.js',
              '/static/resize.js'
        )

        css = {'all' :('http://code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css',)}


    class Meta:
        model = Persons

