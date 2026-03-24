from django.db import models

# Create your models here.
class Notebook(models.Model):
    ESTADOS = [
        ('NUEVO', 'Nuevo'),
        ('USADO', 'Usado'),
        ('MANTENCION', 'En Mantención'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    disponible = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("puede_ver_reporte_interno", "Puede ver reporte interno")
        ]

    def __str__(self):
        return f"{self.codigo} - {self.marca} {self.modelo}"
