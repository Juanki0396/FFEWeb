from django.contrib import admin

# Register your models here.
class InstitutoAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Información', {'fields': ('nombre', 'codigo',)}), 
            ('Dirección', {'fields': ('direccion', 'codigo_postal', 'municipio', 'provincia',)}), 
            ('Ciclos', {'fields': ('ciclos',)}), 
    )
    list_display = ('nombre', 'codigo', 'codigo_postal',)
    search_fields = ('nombre', 'codigo', 'municipio', 'codigo_postal',)
    ordering = ('nombre',)

class InstitutoCicloAdmin(admin.ModelAdmin):
    fieldsets = (
            ('Información', {'fields': ('modalidad',)}), 
            ('Referencias', {'fields': ('insitituto', 'ciclo',)}), 
    )
    list_display = ('ciclo', 'instituto', 'modalidad',)
    list_filter = ( 'modalidad',)
    search_fields = ('instituto', 'ciclo',)
    ordering = ('instituto', 'ciclo',)
