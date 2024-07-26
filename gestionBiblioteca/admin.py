from django.contrib import admin
from .models import Autor, Categoria, Libro, Prestamo

# Register your models here.

class AutorAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'idioma' ,'disponible',)
    list_filter = ('disponible', 'categoria',)
    search_fields = ('titulo',)

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('libro', 'nombre_prestatario', 'fecha_prestamo', 'fecha_devolucion')
    list_filter = ('fecha_prestamo', 'fecha_devolucion')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Prestamo, PrestamoAdmin)