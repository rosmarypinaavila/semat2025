from django.db import models

# Create your models here.
class trabajador (models.Model):
    id = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=15, unique=True,  blank=False)
    nombres = models.CharField(max_length=30,  blank=False)
    Estado_civil = models.CharField(max_length=50,  blank=False)
    direccion = models.CharField(max_length=50,  blank=False)
    telefono =  models.CharField(max_length=15,  blank=True)
    hijos = models.IntegerField()
    estatus = models.BooleanField()

    class Meta:
        ordering = ['-id']
        db_table='trabajador'
    
    def __str__(self):
        return self.cedula

class trabajador_area (models.Model):
    id = models.AutoField(primary_key=True)
    cedulaT = models.ForeignKey(trabajador, on_delete=models.CASCADE, blank=False)
    cargo = models.CharField(max_length=50,  blank=False)
    tipo = (
        ('Empleado', 'Empleado'),
        ('Contratado', 'Contratado'),
    )
    TipoTrab = models.CharField(max_length=20, choices=tipo, default='Empleado')
    area = models.CharField(max_length=30,  blank=False)
    fechaIngreso = models.DateField()
    fechaRetiro = models.DateField()
    observacion = models.TextField(blank=True, null=True)
    estatus = models.BooleanField()

class Cargo_trabajador_gerente (models.Model):
    id = models.AutoField(primary_key=True)
    cedulaT = models.ForeignKey(trabajador, on_delete=models.CASCADE, blank=False)
    cargo = models.CharField(max_length=50,  blank=False)
    fechaCargo = models.DateField()
    resolucion = models.CharField(max_length=30,  blank=False)
    area = models.CharField(max_length=30,  blank=False)
    estatus = models.BooleanField()
