from django.contrib import admin
from .models import Autor, Genero, Libro, InstanciaDeLibro, Lenguaje

admin.site.register(Genero)
admin.site.register(Lenguaje)


class LibroEnLinea(admin.TabularInline):
    model = Libro
    extra = 0


@admin.register(Autor)
class AdminAutor(admin.ModelAdmin):
    list_display = (
        'apellido',
        'nombre',
        'fecha_de_nacimiento',
        'fecha_de_deceso'
    )
    fields = ['nombre', 'apellido', ('fecha_de_nacimiento', 'fecha_de_deceso')]
    inlines = [LibroEnLinea]


class InstanciaDeLibroEnLinea(admin.TabularInline):
    model = InstanciaDeLibro
    extra = 0


@admin.register(Libro)
class AdminLibro(admin.ModelAdmin):
    list_display = (
        'titulo',
        'autor',
        'desplegar_genero',
        'lenguaje'
    )
    inlines = [InstanciaDeLibroEnLinea]


@admin.register(InstanciaDeLibro)
class AdminInstanciaDeLibro(admin.ModelAdmin):
    list_display = (
        'libro',
        'estatus',
        'prestatario',
        'fecha_de_devolucion',
        'id',
    )
    list_filter = ('estatus', 'fecha_de_devolucion')

    readonly_fields = ('id',)
    fieldsets = (
        (None, {
            'fields': ('libro', 'id')
        }),
        ('Disponibilidad', {
            'fields': (
                'estatus',
                'fecha_de_devolucion',
                'prestatario',
            )
        }),
    )

