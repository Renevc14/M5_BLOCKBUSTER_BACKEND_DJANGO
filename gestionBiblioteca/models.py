from django.db import models
from .validators import validar_nombre, validar_fecha
from django.core.exceptions import ValidationError



class Lenguaje(models.TextChoices):
    Ingles = 'IN', 'Ingles'
    Espanol = 'ES', 'Español'

class Autor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, validators=[validar_nombre])
    fecha_nac = models.DateField(validators=[validar_fecha])
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, validators=[validar_nombre])

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    idioma = models.CharField(
        max_length=2,
        choices=Lenguaje.choices,
        default=Lenguaje.Espanol,
    )
    disponible = models.BooleanField(blank=True, default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=100, validators=[validar_nombre])
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado_prestamo = models.BooleanField(blank=True, default=True)
    def clean(self):
        super().clean()
        if self.fecha_devolucion and self.fecha_prestamo and self.fecha_devolucion < self.fecha_prestamo:
            raise ValidationError("La fecha de devolución no puede ser anterior a la fecha de préstamo.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.libro.titulo} prestado a {self.nombre_prestatario}'