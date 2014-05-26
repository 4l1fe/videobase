# coding: utf-8

from django.contrib import admin

from apps.contents.models import *


#############################################################################################################
# Администрирование таблицы контента
class ContentsAdmin(admin.ModelAdmin):
    raw_id_fields = ('film',)


#############################################################################################################
# Администрирование таблицы расположения контента
class LocationsAdmin(admin.ModelAdmin):
    raw_id_fields = ('content',)


#############################################################################################################
# Администрирование таблицы комментариев
class CommentsAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Contents, ContentsAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(About)
admin.site.register(Legal)