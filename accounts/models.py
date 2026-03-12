from django.db import models
from django.contrib.auth.models import AbstractUser

from secrets import token_urlsafe

from ffeweb.choices import Provincia, Rol

# Create your models here.
class Usuario(AbstractUser):

    rol = models.CharField(max_length=3, choices=Rol, default=Rol.ALUMNO)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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

class PerfilTutor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tutoria = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)

class Invitacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, default=token_urlsafe)
    usado = models.BooleanField(default=False)
    rol = models.CharField(max_length=3, choices=Rol)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
