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
    rol = models.CharField(max_length=3, choices=Rol, blank=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return f"{'admin' if self.rol == '' else self.rol} - {self.email}"

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
        return f"ALUMNO:{self.usuario.first_name} {self.usuario.last_name} INS:{self.matricula.instituto_ciclo.instituto.nombre}, FP:{self.matricula.instituto_ciclo.ciclo.nombre}"

class PerfilTutor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tutoria = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

    def __str__(self) -> str:
        return f"TUTOR:{self.usuario.first_name} {self.usuario.last_name} INS:{self.tutoria.instituto_ciclo.instituto.nombre}, FP:{self.tutoria.instituto_ciclo.ciclo.nombre}"

class Invitacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, default=token_urlsafe)
    usado = models.BooleanField(default=False)
    rol = models.CharField(max_length=3, choices=Rol)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()

    def __str__(self) -> str:
        return f"Invitacion de {self.emisor.email} al rol {self.rol} hasta {self.fecha_expiracion}"
