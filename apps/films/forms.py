# coding: utf-8

from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from django.forms import fields

from apps.films.models import Persons, Seasons, Films, FilmExtras
from apps.films.constants import APP_FILM_ADMIN_CSS, APP_FILM_ADMIN_JS_LIBS, APP_FILM_SERIAL


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


#############################################################################################################
#
class PersonsImageForm(ModelForm):
    class Media:
        js = APP_FILM_ADMIN_JS_LIBS
        css = {'all': APP_FILM_ADMIN_CSS}
        
    class Meta:
        model = Persons


#############################################################################################################
#
class FilmExtrasImageForm(ModelForm):
    class Media:
        js =APP_FILM_ADMIN_JS_LIBS
        css = {'all' :APP_FILM_ADMIN_CSS}
        
    class Meta:
        model = FilmExtras


#############################################################################################################
#
class FilmsAdminForm(ModelForm):
    class Media:
        js =APP_FILM_ADMIN_JS_LIBS
        css = {'all' :APP_FILM_ADMIN_CSS}

    class Meta:
        model = Films


#############################################################################################################
# Форма поиска
class SearchForm(Form):
    text     = fields.CharField(max_length='255', required=False)
    genre    = fields.IntegerField(min_value=1, required=False)
    year_old = fields.IntegerField(min_value=1, required=False)
    rating   = fields.FloatField(required=False)
    price    = fields.IntegerField(required=False)
    per_page = fields.IntegerField(min_value=1, required=False, initial=24)
    page     = fields.IntegerField(min_value=1, required=False, initial=1)
    instock  = fields.BooleanField(required=False, initial=False)

    class Meta:
        fields = ('text', 'genre', 'year_old', 'rating', 'price', 'per_page', 'page', 'instock',)


#############################################################################################################
class RatingForm(Form):
    """
    Форма рейтинга для фильмов
    """

    rating = fields.IntegerField(min_value=1, max_value=10, help_text=u'Оценка')


#############################################################################################################
class CommentForm(Form):
    """
    Форма рейтинга для фильмов
    """

    text = fields.CharField(max_length=255, help_text=u'Комментарий')
