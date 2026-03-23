from django.contrib import admin

from .models import CicloFormativo, CursoAcademico, Instituto, InstitutoCiclo, OfertaEducativa

# Register your models here.
@admin.register(Instituto)
class InstitutoAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Información', {'fields': ('nombre', 'codigo',)}), 
            ('Dirección', {'fields': ('direccion', 'codigo_postal', 'municipio', 'provincia',)}), 
    )
    list_display = ('nombre', 'codigo', 'codigo_postal',)
    search_fields = ('nombre', 'codigo', 'municipio', 'codigo_postal',)
    ordering = ('nombre',)

@admin.register(InstitutoCiclo)
class InstitutoCicloAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Información', {'fields': ('modalidad', 'turno',)}), 
            ('Referencias', {'fields': ('instituto', 'ciclo',)}), 
    )
    list_display = ('ciclo__nombre', 'instituto__nombre', 'modalidad', 'turno',)
    list_filter = ( 'modalidad','turno',)
    search_fields = ('instituto__nombre', 'ciclo__nombre',)
    ordering = ('instituto__nombre', 'ciclo__nombre',)

@admin.register(CicloFormativo)
class CicloFormativoAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Información', {'fields': ('nombre', 'codigo',)}), 
    )
    list_display = ('nombre', 'codigo',)
    search_fields = ('nombre', 'codigo',)
    ordering = ('nombre',)

@admin.register(CursoAcademico)
class CursoAcademicoAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {'fields': ('ano_inicio', 'ano_fin',)}), 
    )
    list_display = ('ano_inicio', 'ano_fin',)
    ordering = ('ano_inicio', 'ano_fin',)

@admin.register(OfertaEducativa)
class OfertaEducativaAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {'fields': ('instituto_ciclo', 'curso',)}), 
    )
    list_display = ('instituto_ciclo', 'curso__ano_inicio', 'curso__ano_fin',)
    list_filter = ('instituto_ciclo__modalidad', 'curso',)
    search_fields = ('instituto_ciclo__instituto__nombre', 'instituto_ciclo__ciclo__nombre',)
    ordering = ('curso__ano_inicio', 'instituto_ciclo__instituto__nombre',)
