# coding: utf-8

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from apps.films.models import Persons,Seasons,Films

from apps.films.constants import APP_FILM_ADMIN_CSS,APP_FILM_ADMIN_JS_LIBS


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
        js =APP_FILM_ADMIN_JS_LIBS
        css = {'all' :APP_FILM_ADMIN_CSS}
    class Meta:
        model = Persons

class FilmExtrasImageForm(ModelForm):
    class Media:
        js =APP_FILM_ADMIN_JS_LIBS
        css = {'all' :APP_FILM_ADMIN_CSS}
    class Meta:
        model = Films

