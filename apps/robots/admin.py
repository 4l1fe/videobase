# coding: utf-8

from django.contrib import admin
from .models import *

#############################################################################################################
# Администрирование роботов
class RobotsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Администрирование логирования роботов
class RobotsLogAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Robots, RobotsAdmin)
admin.site.register(RobotsLog, RobotsLogAdmin)
