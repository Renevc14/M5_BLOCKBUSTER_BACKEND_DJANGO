from django.contrib import admin
from .models import Director, Categoria, Pelicula, Prestamo

# Register your models here.

class DirectorAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'director', 'idioma' ,'disponible',)
    list_filter = ('disponible', 'categoria',)
    search_fields = ('titulo',)

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'nombre_prestatario', 'fecha_prestamo', 'fecha_devolucion')
    list_filter = ('fecha_prestamo', 'fecha_devolucion')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Prestamo, PrestamoAdmin)