import re
from django.forms import ValidationError

def validar_telefono(valor):
    if not re.fullmatch(r"^\+?\d{9,16}$", valor):
        raise ValidationError("Introduce número de teléfono válido")

def validar_nif(valor):
    if not re.fullmatch(r"^\d{8}[A-Z]{1}$", valor):
        raise ValidationError("Introduce NIF válido")
