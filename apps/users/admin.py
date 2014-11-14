# coding: utf-8

from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.contrib import admin
from models import *


#############################################################################################################
# Администрирование таблицы пользователей
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email',)
    search_fields = ('id', 'firstname', 'lastname', 'email')
    list_filter = ('created',)
    list_per_page = 30


#############################################################################################################
# Администрирование таблицы пользователей
class UsersProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'created', 'status')
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
    list_display = ('action_time', 'user', 'content_type', 'object_link', 'action_description', 'change_message',)
    change_list_template = 'admin/log_entry_admin/change_list.html'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def action_description(self, obj):
        action_names = {
            ADDITION: 'Addition',
            DELETION: 'Deletion',
            CHANGE: 'Change',
        }
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

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


class FeedAdmin(admin.ModelAdmin):
    pass

#############################################################################################################
# Регистрация моделей в админке
#admin.site.register(User, UsersAdmin)
admin.site.register(UsersProfile, UsersProfileAdmin)
admin.site.register(UsersRels, UsersRelsAdmin)
admin.site.register(UsersPics, UsersPicsAdmin)
# admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Feed, FeedAdmin)
