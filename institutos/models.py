from django.db import models

# Create your models here.
class Modalidad(models.TextChoices):
    NORMAL = 'N', 'Normal'
    INTENSIVO = 'I', 'Intensivo'
    BILINGUE = 'B', 'Bilingüe'

class CicloFormativo(models.Model):
    nombre = models.CharField(max_length=128)
    codigo = models.CharField(max_length=16, unique=True)

class Instituto(models.Model):
    nombre = models.CharField(max_length=128)
    codigo = models.CharField(max_length=8, unique=True)
    direccion = models.CharField(max_length=256)
    ciclos = models.ManyToManyField(CicloFormativo, through='InstitutoCiclo')
    usuario = models.OneToOneField('accounts.Usuario', on_delete=models.CASCADE)

class InstitutoCiclo(models.Model):
    ciclo = models.ForeignKey(CicloFormativo, on_delete=models.CASCADE)
    instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
    modalidad = models.CharField(max_length=1, choices=Modalidad)
