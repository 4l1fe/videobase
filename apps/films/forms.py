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
    year_old = fields.IntegerField(min_value=0, required=False)
    rating   = fields.FloatField(required=False)
    price    = fields.FloatField(min_value=0, required=False)
    per_page = fields.IntegerField(initial=24, min_value=1)
    page     = fields.IntegerField(initial=1, min_value=1)
    instock  = fields.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        if not kwargs['data'].get('page'):
           kwargs['data']['page'] = 1

        if not kwargs['data'].get('per_page'):
           kwargs['data']['per_page'] = 24

        super(SearchForm, self).__init__(*args, **kwargs)

        for k,v in self.fields.items():
            if k in kwargs['data'] and self.fields[k].required==False:
                self.fields[k].required = True

    def clean_per_page(self):
        if 'per_page' in self.cleaned_data:
            if self.cleaned_data['per_page'] > 30:
                return 24
            return self.cleaned_data['per_page']

    def clean_text(self):
        if 'text' in self.cleaned_data:
            self.cleaned_data['name'] = self.cleaned_data['text']
            return self.cleaned_data['text']

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


#############################################################################################################
class DetailForm(Form):
    """
    Форма детализация для vbFilm
    """

    extend  = fields.BooleanField(initial=False, required=False, help_text=u'Расширенный')
    persons = fields.BooleanField(initial=False, required=False, help_text=u'Персоны')
