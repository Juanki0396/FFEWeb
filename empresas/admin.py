from django.contrib import admin

from .models import Empresa, RepresentanteLegal


class RepresentanteLegalInline(admin.StackedInline):
    model = RepresentanteLegal
    extra = 0


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identificación', {'fields': ('cif', 'nombre', 'entidad_juridica')}),
        ('Contacto', {'fields': ('telefono',)}),
        ('Dirección', {'fields': ('direccion', 'codigo_postal', 'municipio', 'provincia', 'pais')}),
    )
    list_display = ('nombre', 'cif', 'municipio', 'provincia')
    search_fields = ('nombre', 'cif', 'municipio', 'codigo_postal')
    ordering = ('nombre',)
    inlines = [RepresentanteLegalInline]


@admin.register(RepresentanteLegal)
class RepresentanteLegalAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos personales', {'fields': ('nombre', 'apellidos', 'nif', 'cargo')}),
        ('Empresa', {'fields': ('empresa',)}),
        ('Documentación', {'fields': ('base_normativa', 'efectuado_por')}),
    )
    list_display = ('apellidos', 'nombre', 'nif', 'cargo', 'empresa')
    search_fields = ('nif', 'nombre', 'apellidos', 'empresa__nombre')
    ordering = ('empresa__nombre', 'apellidos')
