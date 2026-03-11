from django.db import models

# Create your models here.
class Rol(models.TextChoices):
    ALUMNO = 'alumno', 'Alumno'
    TUTOR = 'tutor', 'Tutor'
    EMPRESA = 'empresa', 'Empresa'

