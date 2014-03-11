from django.contrib import admin
from content.models import Content,Locations,Comments


class ContentAdmin(admin.ModelAdmin):
    pass

class LocationsAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Content, ContentAdmin)
admin.site.register(Locations, LocationsAdmin)
admin.site.register(Comments, CommentsAdmin)

        
        



