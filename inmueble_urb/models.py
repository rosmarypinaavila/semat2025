from django.db import models
from pathlib import Path
from django.conf import settings 
from django.utils.text import slugify
from tramites.models import Contribuyente
from tramites.models import tram_solv_inm


# Create your models here.
class Inmuebles_all(models.Model):
    id_inmu = models.AutoField(primary_key=True)
    codigo_sap = models.CharField(max_length=15, unique=True)
    codigo_cast = models.CharField(max_length=50, unique=True, blank=True)
    carpeta = models.CharField(unique = True, max_length=100, editable=False, blank=True)
    contribuye_Inmu = models.ForeignKey(Contribuyente, on_delete=models.CASCADE)
    nombre_contr = models.CharField(max_length=150, null=True)
    dir_inmueble = models.TextField(max_length=250, blank=True, null=True)
    fecha_reg = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Inmuebles_all')
    altitud = models.CharField(max_length=15, null=True)
    latitud = models.CharField(max_length=15, null=True) 
    
    status = models.BooleanField(default=True)

    class Meta:
        db_table='inm_info'
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # es inserción si no tiene PK aún

        super().save(*args, **kwargs)  # guarda para obtener PK si es nuevo

        if is_new:
            # Usar cod catastral o PK para la ruta
            catas = self.codigo_sap or 'default'
            safe_cat = slugify(str(catas))

            # Si quieres usar PK en la ruta, podrías hacer:
            # ruta_base = Path(settings.MEDIA_ROOT) / 'inmuebles' / str(self.pk)

            ruta_base = Path(settings.MEDIA_ROOT) / 'inmuebles' / safe_cat
            ruta_base.mkdir(parents=True, exist_ok=True)

            self.carpeta = str(ruta_base.relative_to(settings.MEDIA_ROOT))
            super().save(update_fields=['carpeta'])


    def __str__(self):
        return self.codigo_sap
    
def carpeta_inmueble_upload_to(instance, filename):
    # Accedemos a la licencia a través de la relación con Empresas
    if instance.Inmueble and instance.Inmueble.codigo_sap:
        lic = slugify(str(instance.Inmueble.codigo_sap))
        return f'inmuebles/{lic}/{filename}'
    else:
        # Fallback por si no hay empresa asociada
        return f'inmuebles/default/{filename}'


class Inmueble_cod_sap(models.Model):
    Inmueble_sap = models.ForeignKey(Inmuebles_all, on_delete=models.CASCADE)
    cedula = models.FileField(upload_to=carpeta_inmueble_upload_to, null=True, blank=True)
    avaluo = models.FileField(upload_to=carpeta_inmueble_upload_to, null=True, blank=True)
    rif = models.FileField(upload_to=carpeta_inmueble_upload_to, null=True, blank=True)
    contrato = models.FileField(upload_to=carpeta_inmueble_upload_to, null=True, blank=True)
    escritura = models.FileField(upload_to=carpeta_inmueble_upload_to, null=True, blank=True)
    boletinCatast = models.FileField(upload_to=carpeta_inmueble_upload_to, blank=True)
       
class Inm_Solvencia(models.Model):
    id = models.AutoField(primary_key=True)
    n_control_Inm= models.CharField(max_length=10, unique=True)
    cod_catas = models.ForeignKey(Inmuebles_all, on_delete=models.CASCADE, null= False)
    nomb_contribuyente= models.CharField(max_length=200, blank=False)
    direcc = models.CharField(max_length=120, blank=False)
    num_tramite_In = models.ForeignKey(tram_solv_inm, on_delete=models.CASCADE, null= False)
    fecha_exp = models.DateField(auto_now_add=True)
    n_planilla = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField(blank=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Inm_Solvencia')
    observ_2 = models.TextField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=True)


    class Meta:
        db_table = 'inm_solvencia'
        ordering = ['-n_control_Inm']
    
    def __str__(self):
        return str(self.n_control_Inm)