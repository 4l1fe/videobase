# coding: utf-8

from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.contrib import admin
from models import *


#############################################################################################################
# Администрирование таблицы пользователей
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'created', 'ustatus')
    search_fields = ('id', 'firstname', 'lastname', 'email')
    list_filter = ('created',)
    list_per_page = 30


#############################################################################################################
# Отношения пользователей
class UsersRelsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Аминистрирование таблицы загружаемых картинок пользователей
class UsersPicsAdmin(admin.ModelAdmin):
    pass


#############################################################################################################
# Лог админки
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = LogEntry._meta.get_all_field_names()
    list_filter = ('user', 'content_type', 'action_flag',)
    search_fields = ('object_repr', 'change_message',)
    list_display = ('action_time', 'user', 'content_type', 'object_link', 'action_flag', 'change_message',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False
    #
    # def formfield_for_choice_field(self, db_field, request, **kwargs):
    #     if db_field.name == "action_flag":
    #         kwargs['choices'] = (
    #             (1, 'Add'),
    #             (2, 'Change'),
    #             (3, 'Delete'),
    #         )
    #
    #     return super(LogEntryAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
    #
    # def action_flag_name(self, obj):
    #     if obj.is_addition():
    #         return "Add"
    #     elif obj.is_change():
    #         return "Change"
    #     else:
    #         return "Delete"
    #
    # action_flag_name.short_description = self

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request).select_related('content_type')


#############################################################################################################
# Регистрация моделей в админке
admin.site.register(Users, UsersAdmin)
admin.site.register(UsersRels, UsersRelsAdmin)
admin.site.register(UsersPics, UsersPicsAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
