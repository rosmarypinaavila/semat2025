from django.db import models
from pathlib import Path
from django.conf import settings
from django.utils.text import slugify 
from tramites.models import *


# Create your models here.
class MarcaVehiculo (models.Model):
    idMarca = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length= 30, blank=False)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Marca_vehi'
        ordering = ['-idMarca']
    
    def __str__(self):
        return self.descripcion


class ModeloVehiculo (models.Model):
    idModelo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length= 30, blank=False)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Modelo_vehi'
        ordering = ['-idModelo']
    
    def __str__(self):
        return self.descripcion


class vehiculos (models.Model):
    id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=30, unique=True, blank=False)
    carpeta = models.CharField(unique = True, max_length=100, editable=False, blank=True)
    modeloVehi = models.ForeignKey(ModeloVehiculo,  on_delete=models.CASCADE, blank=False)
    marcaVehi = models.ForeignKey(MarcaVehiculo,  on_delete=models.CASCADE, blank=False)
    año = models.IntegerField( blank= False)
    fecha_reg = models.DateField(auto_now_add=True)
    contribuyen = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, blank=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehiculo_all')
    cedula_func = models.CharField(max_length=15, blank= True)
    nomb_func = models.CharField(max_length=30, blank= True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'vehiculo'
        ordering = ['-placa']

    def save(self, *args, **kwargs):
            is_new = self.pk is None  # es inserción si no tiene PK aún

            super().save(*args, **kwargs)  # guarda para obtener PK si es nuevo

            if is_new:
               # Usar placa o PK para la ruta
               plac = self.placa or 'default'
               safe_plac = slugify(str(plac))

               # Si quieres usar PK en la ruta, podrías hacer:
               # ruta_base = Path(settings.MEDIA_ROOT) / 'vehiculos' / str(self.pk)

               ruta_base = Path(settings.MEDIA_ROOT) / 'vehiculos' / safe_plac
               ruta_base.mkdir(parents=True, exist_ok=True)

               self.carpeta = str(ruta_base.relative_to(settings.MEDIA_ROOT))
               super().save(update_fields=['carpeta'])

        
    def __str__(self):
           return self.placa
    
def carpeta_vehiculo_upload_to(instance, filename):
    # Accedemos a la placa a través de la relación con Vehiculos
    if instance.Vehiculo and instance.Vehiculo.placa:
        plac = slugify(str(instance.Vehiculo.placa))
        return f'vehiculos/{plac}/{filename}'
    else:
        # Fallback por si no hay vehiculo asociada
        return f'vehiculos/default/{filename}'


class Vehiculos_placa(models.Model):
    Vehiculo = models.ForeignKey(vehiculos, on_delete=models.CASCADE)
    placaV = models.FileField (upload_to = carpeta_vehiculo_upload_to)    
    
    def __str__(self):
        # Retorna la placa del vehículo como string
        return str(self.Vehiculo.placa) if self.Vehiculo and self.Vehiculo.placa else "Sin vehículo asociado"
    
class vehi_Solvencia(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_reg = models.DateField(auto_now_add=True)
    n_control_Vehi= models.CharField(max_length=50, unique=True, blank=True)
    num_tramite_Veh = models.ForeignKey(tram_solv_veh, on_delete=models.CASCADE, null= False)
    n_placa_Vehi= models.ForeignKey(vehiculos, on_delete=models.CASCADE)
    contribuyente= models.CharField(max_length=200, blank=False)
    n_planilla = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField(blank=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehi_Solvencia')
    observ_2 = models.TextField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'veh_Solvencia'
        ordering = ['-n_placa_Vehi']
    
    def __str__(self):
        return str(self.n_placa_Vehi)


