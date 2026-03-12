from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Usuario(AbstractUser):

    class Rol(models.TextChoices):
        ALUMNO = 'A', 'Alumno'
        TUTOR = 'T', 'Tutor'
        EMPRESA = 'E', 'Empresa'
        INSTITUTO = 'I', 'Instituto'

    rol = models.CharField(max_length=1, choices=Rol, default=Rol.ALUMNO)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class PerfilAlumno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    pais_nacimiento =  models.CharField(max_length=64)
    nif = models.CharField(max_length=9, unique=True)
    direccion =  models.CharField(max_length=128)
    codigo_postal =  models.CharField(max_length=16)
    municipio =  models.CharField(max_length=64)
    provincia =  models.CharField(max_length=64)
    matricula = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)

class PerfilTutor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tutoria = models.ForeignKey('institutos.OfertaEducativa', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16, unique=True)

