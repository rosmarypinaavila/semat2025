from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User

from act_econ.models import *

# Create your models here.

class Empresas_licencia_Publicidad(models.Model):
    Empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=carpeta_empresa_upload_to)

class publicidad_Solvencia(models.Model):
    idSolv = models.AutoField(primary_key=True)
    n_control= models.CharField(max_length=50, unique=True, blank=True)
    licencia= models.ForeignKey(Empresas, on_delete=models.CASCADE, max_length=20, blank=True)
    contribuyente = models.CharField(max_length=150, blank=True)
    documento = models.CharField(max_length=20, blank=True)
    direcc = models.CharField(max_length=150, blank=True)
    n_planilla = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField(blank=False)
    fecha_exp = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solvencias_publicidad')
    solicitud_solv = models.ForeignKey(tram_solv_pub, on_delete=models.CASCADE, max_length=20, blank=True)
    observacion = models.CharField(max_length=120, blank=True)
    status = models.BooleanField(default=True)


    class Meta:
        db_table = 'publici_solvencia'
        ordering = ['-n_control']

    def __str__(self):
        return str(self.n_control)