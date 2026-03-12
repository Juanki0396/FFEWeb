from django.db import models

from ffeweb.choices import Provincia

# Create your models here.
class Empresa(models.Model):
    cif = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=128)
    direccion =  models.CharField(max_length=128)
    codigo_postal =  models.CharField(max_length=16)
    municipio =  models.CharField(max_length=64)
    provincia =  models.CharField(max_length=2, choices=Provincia, blank=True)
    pais =  models.CharField(max_length=64)
    entidad_juridica =  models.CharField(max_length=64)
    telefono = models.CharField(max_length=16)

class RepresentanteLegal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64)
    apellidos = models.CharField(max_length=128)
    nif = models.CharField(max_length=9, unique=True)
    cargo = models.CharField(max_length=64)
    base_normativa = models.TextField()
    efectuado_por = models.TextField()

class TutorEmpresa(models.Model):
    usuario = models.OneToOneField('accounts.Usuario', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=16)
