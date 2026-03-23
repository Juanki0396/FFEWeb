from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from secrets import token_urlsafe

from ffeweb.choices import Provincia, Rol

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class PerfilAlumno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    pais_nacimiento =  models.CharField(max_length=64, default='')
    nif = models.CharField(max_length=9, unique=True, default='')
    direccion =  models.CharField(max_length=128, default='')
    codigo_postal =  models.CharField(max_length=16, default='')
    municipio =  models.CharField(max_length=64, default='')
    provincia =  models.CharField(max_length=2, choices=Provincia, default='')
    matricula = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"ALUMNO({self.usuario.first_name} {self.usuario.last_name}, {self.matricula.instituto_ciclo.instituto.nombre}, {self.matricula.instituto_ciclo.ciclo.nombre})"

class PerfilTutor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tutoria = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"TUTOR({self.usuario.first_name} {self.usuario.last_name}, {self.tutoria.instituto_ciclo.instituto.nombre}, {self.tutoria.instituto_ciclo.ciclo.nombre})"

class PerfilAdminInstituto(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    instituto = models.ForeignKey('institutos.Instituto', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"ADMIN_INSTITUTO({self.usuario.first_name} {self.usuario.last_name}, {self.instituto.nombre})"

class PerfilTutorEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"TUTOR_EMPRESA({self.usuario.first_name} {self.usuario.last_name}, {self.empresa.nombre})"

class PerfilAdminEmpresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"ADMIN_EMPRESA({self.usuario.first_name} {self.usuario.last_name}, {self.empresa.nombre})"

class Invitacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    receptor = models.EmailField(blank=True, default='')
    token = models.CharField(max_length=64, unique=True, default=token_urlsafe)
    usado = models.BooleanField(default=False)
    rol = models.CharField(max_length=3, choices=Rol)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    instituto = models.ForeignKey('institutos.Instituto', null=True, blank=True, on_delete=models.SET_NULL)                                                                    
    empresa = models.ForeignKey('empresas.Empresa', null=True, blank=True, on_delete=models.SET_NULL)                                                                    
    oferta_educativa = models.ForeignKey('institutos.OfertaEducativa', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"INVITATION({self.emisor.email}, {self.rol}, {self.fecha_expiracion})"
