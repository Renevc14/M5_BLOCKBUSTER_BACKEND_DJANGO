from django.core.exceptions import ValidationError
from datetime import date

def validar_nombre(value):
    if int(len(value)) <= 2:
        raise ValidationError(f"{value} debe tener al menos 3 caracteres")

def validar_fecha(value):
    if (value > date(2009, 12, 31)):
        raise ValidationError("La fecha de nacimiento debe ser anterior al 1 de enero de 2010.")