from django.contrib import admin
from models import Films, Countries, Genres,Seasons



# Register your models here.

class FilmsAdmin(admin.ModelAdmin):
    pass
class GenresAdmin(admin.ModelAdmin):
    pass
class CountriesAdmin(admin.ModelAdmin):
    pass
class SeasonsAdmin(admin.ModelAdmin):
    pass

    
    
admin.site.register(Films, FilmsAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Seasons, SeasonsAdmin)
