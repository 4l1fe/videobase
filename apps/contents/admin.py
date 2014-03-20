# coding: utf-8

from django.contrib import admin

from apps.contents.models import *


#############################################################################################################
# Администрирование таблицы контента
class ContentsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы расположения контента
class LocationsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование таблицы комментариев
class CommentsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Contents, ContentsAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(Comments, CommentsAdmin)
