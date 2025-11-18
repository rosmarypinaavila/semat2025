from django.db import models
from pathlib import Path
from django.conf import settings 
from django.utils.text import slugify
from tramites.models import *

# Create your models here.



class Empresas(models.Model):
    id = models.AutoField(primary_key=True)
    licencia = models.CharField(unique=True, max_length=15)
    carpeta = models.CharField(unique = True, max_length=100, editable=False, blank=True)
    documento = models.CharField(max_length=15, blank=False)
    razon_social = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    observacion = models.CharField(max_length=250, blank=True)
    fecha_reg = models.DateField(auto_now_add=True)
    contribuyentes = models.ForeignKey(Contribuyente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresas_actecon')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'ae_empresas'
        ordering = ['-licencia']
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # es inserción si no tiene PK aún

        super().save(*args, **kwargs)  # guarda para obtener PK si es nuevo

        if is_new:
            # Usar licencia o PK para la ruta
            lic = self.licencia or 'default'
            safe_lic = slugify(str(lic))

            # Si quieres usar PK en la ruta, podrías hacer:
            # ruta_base = Path(settings.MEDIA_ROOT) / 'empresas' / str(self.pk)

            ruta_base = Path(settings.MEDIA_ROOT) / 'empresas' / safe_lic
            ruta_base.mkdir(parents=True, exist_ok=True)

            self.carpeta = str(ruta_base.relative_to(settings.MEDIA_ROOT))
            super().save(update_fields=['carpeta'])

        
    def __str__(self):
        return self.licencia
    
def carpeta_empresa_upload_to(instance, filename):
    # Accedemos a la licencia a través de la relación con Empresas
    if instance.Empresa and instance.Empresa.licencia:
        lic = slugify(str(instance.Empresa.licencia))
        return f'empresas/{lic}/{filename}'
    else:
        # Fallback por si no hay empresa asociada
        return f'empresas/default/{filename}'


class Empresas_licencia(models.Model):
    Empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    registro_Merca = models.FileField(upload_to= carpeta_empresa_upload_to, null=True , blank= True)
    rif = models.FileField(upload_to= carpeta_empresa_upload_to, null=True, blank=True) 
    cedula_repre = models.FileField(upload_to= carpeta_empresa_upload_to, null = True, blank=True )
    licenciaE = models.FileField (upload_to = carpeta_empresa_upload_to, null= True, blank=True)

class Act_econ_Solvencia(models.Model):
    idSolv = models.AutoField(primary_key=True)
    n_control= models.CharField(max_length=50, unique=True, blank=True)
    licencia = models.ForeignKey(Empresas, on_delete=models.CASCADE, max_length=20, blank=True)
    contribuyente = models.CharField(max_length=150, blank=True)
    documento = models.CharField(max_length=20, blank=True)
    direcc = models.CharField(max_length=150, blank=True)
    n_planilla = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField(blank=False)
    fecha_exp = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solvencias_actecon')
    solicitud_solv = models.ForeignKey(tram_solv_actecon, on_delete=models.CASCADE, max_length=20, blank=True)
    observacion = models.CharField(max_length=120, blank=True)
    status = models.BooleanField(default=True)


    class Meta:
        db_table = 'ae_solvencia'
        ordering = ['-n_control']

    def __str__(self):
        return str(self.n_control)
    
class Act_econ_no_contribuyente(models.Model):
    id = models.AutoField(primary_key=True)
    n_control = models.CharField(max_length=50, unique=True, blank=True)
    nombre = models.CharField(max_length=120, blank=False)
    cedula = models.CharField(max_length=20, blank=False)
    n_planilla = models.CharField(max_length=50, blank=False)
    fecha_exp = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='no_contribuyentes_actecon')
    status = models.BooleanField(default=True)


    class Meta:
        db_table = 'ae_no_contribuyente'
        ordering = ['-n_control']

    def __str__(self):
        return str(self.n_control)
    
class Act_econ_constancia(models.Model):
    idc = models.AutoField(primary_key=True)
    n_control_const = models.CharField(max_length=50, unique=True, blank=True)
    licencia = models.ForeignKey(Empresas, on_delete=models.CASCADE, max_length=20, blank=True)
    nomb_empresa = models.CharField(max_length=150, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    fecha_exp = models.DateField(auto_now_add=True)
    planilla = models.CharField(max_length=50, blank=False)
    fecha_plan = models.DateField(blank=False)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='constancias_actecon')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'ae_constancia'
        ordering = ['-idc']

    def __str__(self):
        return str(self.idc)
    
class Act_econ_ivss_act(models.Model):
    id = models.AutoField(primary_key=True)
    n_control = models.CharField(max_length=50, blank=True, null=True)
    num_solicitud_ivssAct = models.ForeignKey(tram_ivss_reg, on_delete= models.CASCADE, max_length=20, blank= False)
    licencia = models.ForeignKey(Empresas, on_delete=models.CASCADE, max_length=20, blank=True)
    rif = models.CharField(max_length=30, blank=True)
    nomb_empresa = models.CharField(max_length=250, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=150, blank=False)
    documento = models.CharField(max_length=30, blank=False)
    planilla = models.CharField(max_length=50, blank=False)
    fecha_plan = models.DateField(null=True)
    fecha_exp = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ivss_actecon')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'ae_conts_ivss_act'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)
    
class Act_econ_ivss_noreg(models.Model):
    id = models.AutoField(primary_key=True)
    n_control = models.CharField(max_length=50, null=True, blank=True)
    num_solicitud_ivssAct = models.ForeignKey(tram_ivss_noreg, on_delete= models.CASCADE, max_length=20, blank= False)
    nombre = models.CharField(max_length=150, blank=False)
    documento = models.CharField(max_length=30, blank=False)
    empresas = models.CharField(max_length=250, blank=False)
    planilla = models.CharField(max_length=50, blank=False)
    fecha_plan = models.DateField(null=True)
    fecha_exp = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ivss_noreg_actecon')
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'ae_conts_ivss_nrg'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)
