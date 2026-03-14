from django.db import models

from ffeweb.choices import Provincia

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
    direccion =  models.CharField(max_length=128, default='')
    codigo_postal =  models.CharField(max_length=16, default='')
    municipio =  models.CharField(max_length=64, default='')
    provincia =  models.CharField(max_length=2, choices=Provincia, default='')
    ciclos = models.ManyToManyField(CicloFormativo, through='InstitutoCiclo')

class InstitutoCiclo(models.Model):
    ciclo = models.ForeignKey(CicloFormativo, on_delete=models.CASCADE)
    instituto = models.ForeignKey(Instituto, on_delete=models.CASCADE)
    modalidad = models.CharField(max_length=1, choices=Modalidad)

class CursoAcademico(models.Model):
    ano_inicio = models.IntegerField()
    ano_fin = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.ano_inicio}-{self.ano_fin}"

class OfertaEducativa(models.Model):
    instituto_ciclo = models.ForeignKey(InstitutoCiclo, on_delete=models.CASCADE)
    curso = models.ForeignKey(CursoAcademico, on_delete=models.CASCADE)

