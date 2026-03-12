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
