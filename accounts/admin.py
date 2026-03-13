from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario, PerfilAlumno, PerfilTutor, Invitacion
from empresas.models import Empresa, TutorEmpresa
from institutos.models import 
from ffeweb.choices import Rol

# Register your models here.
class PerfilAlumnoInline(admin.StackedInline):
    model = PerfilAlumno
    can_delete = False

class PerfilTutorInline(admin.StackedInline):
    model = PerfilAlumno
    can_delete = False

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('FFE', {'fields': ('rol', 'email_verified')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2', 'rol')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('email',)

    def get_inlines(self, request, obj=None):
        if obj and obj.rol == Rol.ALUMNO:
            return [PerfilAlumnoInline]
        elif obj and obj.rol == Rol.TUTOR:
            return [PerfilTutorInline]
        return []

@admin.register(PerfilAlumno)
class PerfilAlumnoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('usuario',)}),
        ('Información personal', {'fields': ('nif', 'fecha_nacimiento', 'pais_nacimiento')}),
        ('Domicilio', {'fields': ('direccion', 'codigo_postal', 'municipio', 'provincia')}),
        ('matricula', {'fields': ('matricula',)}),
    )
    list_display = ('usuario', 'nif', )
    list_filter = ('matricula__instituto_ciclo__instituto__nombre',)
    search_fields = ('nif', 'usuario__email',)
    ordering = ('matricula__instituto_ciclo__instituto__nombre', 'matricula__instituto_ciclo__ciclo__nombre')

@admin.register(PerfilTutor)
class PerfilTutorAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('usuario', 'telefono',)}),
        ('Tutoria', {'fields': ('tutoria',)}),
    )
    list_display = ('usuario', 'tutoria', )
    search_fields = ('usuario__email',)
    ordering = ('usuario__email',)


@admin.register(Invitacion)
class InvitacionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('emisor', 'rol', 'token', 'fecha_creacion', 'fecha_expiracion')}),
    )
    list_display = ('token', 'emisor', 'usado', 'fecha_expiracion' )
    list_filter = ('rol', 'usado',)
    search_fields = ('emisor__email', 'token',)
    readonly_fields = ('token', 'fecha_creacion')
    ordering = ('fecha_creacion',)
