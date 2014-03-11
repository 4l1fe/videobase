from django.contrib import admin
from apps.films.models import  Countries,Genres,Films,UsersFilms,FilmExtras,Seasons


class CountriesAdmin(admin.ModelAdmin):
    pass
    
class GenresAdmin(admin.ModelAdmin):
    pass
    
class FilmsAdmin(admin.ModelAdmin):
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
admin.site.register(UsersFilms,UserFilmsAdmin)
admin.site.register(FilmExtras,FilmExtrasAdmin)
admin.site.register(Seasons,SeasonsAdmin)


