from django.contrib import admin
from films import Countries, Genres, Films, UserFilms, FilmExtras, Seasons
# Register your models here.


class CountriesAdmin(admin.ModelAdmin):
    pass
    
class GenresAdmin(admin.ModelAdmin):
    pass
    
class FilmsAdmin(admin.ModelAdmin):
    pass
    
class FilmAdmin(admin.ModelAdmin):
    pass
    
class UserFilmsAdmin(admin.ModelAdmin):
    pass
    
class FilmExtrasAdmin(admin.ModelAdmin):
    pass
    
class SeasonsAdmin(admin.ModelAdmin):
    pass
    

admin.site.register(Countries,CountriesAdmin)
admin.site.register(Genres,GenresAdmin)
admin.site.register(Films,FilmsAdmin)
admin.site.register(UserFilms,UserFilmsAdmin)
admin.site.register(FilmExtras,FilmExtrasAdmin)
admin.site.register(Seasons SeasonsAdmin)

