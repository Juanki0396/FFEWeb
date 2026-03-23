from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Usuario, PerfilAlumno, PerfilTutor, PerfilAdminInstituto,PerfilTutorEmpresa, PerfilAdminEmpresa, Invitacion

# Register your models here.
class PerfilAlumnoInline(admin.StackedInline):
    model = PerfilAlumno
    can_delete = False

class PerfilTutorInline(admin.StackedInline):
    model = PerfilTutor
    can_delete = False

class PerfilAdminInstitutoInline(admin.StackedInline):
    model = PerfilAdminInstituto
    can_delete = False

class PerfilTutorEmpresaInline(admin.StackedInline):
    model = PerfilTutorEmpresa
    can_delete = False

class PerfilAdminEmpresaInline(admin.StackedInline):
    model = PerfilAdminEmpresa
    can_delete = False

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'email_verified',)}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ( 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login', 'email_verified',)
    ordering = ('email',)

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if hasattr(obj, 'perfilalumno'):
            return [PerfilAlumnoInline]
        elif hasattr(obj, 'perfiltutor'):
            return [PerfilTutorInline]
        elif hasattr(obj, 'perfiladmininstituto'):
            return [PerfilAdminInstitutoInline]
        elif hasattr(obj, 'perfiltutorempresa'):
            return [PerfilTutorEmpresaInline]
        elif hasattr(obj, 'perfiladminempresa'):
            return [PerfilAdminEmpresaInline]
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

@admin.register(PerfilAdminInstituto)
class PerfilAdminInstitutoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('usuario', 'telefono',)}),
        ('Instituto', {'fields': ('instituto',)}),
    )
    list_display = ('usuario', 'instituto', )
    search_fields = ('usuario__email',)
    ordering = ('usuario__email',)

@admin.register(PerfilTutorEmpresa)
class PerfilTutorEmpresaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('usuario', 'telefono',)}),
        ('Empresa', {'fields': ('empresa',)}),
    )
    list_display = ('usuario', 'empresa', )
    search_fields = ('usuario__email',)
    ordering = ('usuario__email',)

@admin.register(PerfilAdminEmpresa)
class PerfilAdminEmpresaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('usuario', 'telefono',)}),
        ('Empresa', {'fields': ('empresa',)}),
    )
    list_display = ('usuario', 'empresa', )
    search_fields = ('usuario__email',)
    ordering = ('usuario__email',)

@admin.register(Invitacion)
class InvitacionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos', {'fields': ('emisor', 'receptor', 'rol', 'token', 'fecha_creacion', 'fecha_expiracion')}),
        ('Contexto', {'fields': ('instituto', 'empresa', 'oferta_educativa',)}),

    )
    list_display = ('token', 'emisor', 'receptor', 'usado', 'fecha_expiracion' )
    list_filter = ('rol', 'usado',)
    search_fields = ('emisor__email', 'token',)
    readonly_fields = ('emisor', 'token', 'fecha_creacion')
    ordering = ('fecha_creacion',)

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.emisor = request.user
        super().save_model(request, obj, form, change)
        if not change and obj.receptor:
            url = reverse('invitacion_registro', args=[obj.token])
            context = {
                'url': url,
                'rol': obj.get_rol_display(),
                'emisor': obj.emisor,
            }
            html = render_to_string('accounts/emails/invitacion.html', context)
            text = f"Has sido invitado a registrarte en FFEWeb. Accede a: {url}"
            email = EmailMultiAlternatives(
                subject='Invitación para registrarte en FFEWeb',
                body=text,
                from_email=None,
                to=[obj.receptor],
            )
            email.attach_alternative(html, 'text/html')
            email.send()
