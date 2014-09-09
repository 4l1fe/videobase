# coding: utf-8

from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from django.forms import fields

from apps.films.constants import APP_FILM_PERSON_TYPES_OUR
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
    text      = fields.CharField(max_length='255', required=False)
    genre     = fields.IntegerField(min_value=0, required=False)
    year_old  = fields.IntegerField(min_value=0, required=False)
    rating    = fields.FloatField(min_value=0, required=False)
    price     = fields.FloatField(min_value=0, required=False)
    instock   = fields.BooleanField(required=False)
    recommend = fields.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        for k,v in self.fields.items():
            if k in kwargs['data'] and kwargs['data'][k]:
                if self.fields[k].required == False:
                    self.fields[k].required = True

    class Meta:
        fields = ('text', 'genre', 'year_old', 'rating', 'price', 'instock',)


#############################################################################################################
class RatingForm(Form):
    """
    Форма рейтинга для фильмов
    """

    rating = fields.FloatField(min_value=1.0, max_value=10.0, help_text=u'Оценка')


#############################################################################################################
class CommentForm(Form):
    """
    Форма для комментария к фильму
    """

    text = fields.CharField(min_length=20, max_length=8000, help_text=u'Комментарий')


#############################################################################################################
class DetailForm(Form):
    """
    Форма детализация для vbFilm
    """

    extend  = fields.BooleanField(initial=False, required=False, help_text=u'Расширенный')
    persons = fields.BooleanField(initial=False, required=False, help_text=u'Персоны')


#############################################################################################################
class PersonApiForm(Form):
    """
    Форма для проверки vbPerson
    """

    type  = fields.ChoiceField(choices=APP_FILM_PERSON_TYPES_OUR, help_text=u'Тип')
    top   = fields.IntegerField(min_value=0, help_text=u'Сортировать с')
    limit = fields.IntegerField(required=False, min_value=1, help_text=u'Ограничение')

    def __init__(self, *args, **kwargs):
        if not kwargs['data'].get('top'):
           kwargs['data']['top'] = 0

        if not kwargs['data'].get('type'):
           kwargs['data']['type'] = 'all'

        super(PersonApiForm, self).__init__(*args, **kwargs)

        for k,v in self.fields.items():
            if k in kwargs['data'] and kwargs['data'][k]:
                if self.fields[k].required == False:
                    self.fields[k].required = True


#############################################################################################################
class PersonFilmographyApiForm(Form):
    """Форма для валидации в PersonFilmographyAPIView
    """
    type = fields.ChoiceField(choices=APP_FILM_PERSON_TYPES_OUR, help_text=u'Тип')
    page = fields.IntegerField(initial=1, min_value=1)
    per_page = fields.IntegerField(initial=12, min_value=1)

    def __init__(self, *args, **kwargs):
        if not kwargs['data'].get('page'):
           kwargs['data']['page'] = 1

        if not kwargs['data'].get('per_page'):
           kwargs['data']['per_page'] = 12

        if not kwargs['data'].get('type'):
           kwargs['data']['type'] = 'all'

        super(PersonFilmographyApiForm, self).__init__(*args, **kwargs)
        
