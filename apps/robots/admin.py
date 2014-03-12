# coding: utf-8

from django.contrib import admin
from .models import *

#############################################################################################################
# Администрирование роботов
class RobotsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False

    def __init__(self, *args, **kwargs):
        super(RobotsAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)


#############################################################################################################
# Администрирование логирования роботов
class RobotsLogAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request):
        return False

    def __init__(self, *args, **kwargs):
        super(RobotsLogAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Robots, RobotsAdmin)
admin.site.register(RobotsLog, RobotsLogAdmin)
