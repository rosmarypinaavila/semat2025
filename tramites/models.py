from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

# Create your models here.


class Contribuyente(models.Model):
    TIPO_CONTRIBUYENTE = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
        ('fpersonal', 'Firma Personal'),
        ('EGubernamental', 'Organismo o ente Gubernamental'),
        ('emprendedor', 'Emprendedor'),

    ]
    ced_rif = models.CharField(max_length=13, unique=True)
    tipo_contribuyente = models.CharField(max_length=15, choices=TIPO_CONTRIBUYENTE, default='natural')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    identificacion = models.CharField(max_length=50, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    users = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_contribuyente')

    def __str__(self):
        return f"{self.users.username} - {self.ced_rif}"

# Signal para crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil_contribuyente(sender, instance, created, **kwargs):
    if created and not instance.is_staff:  # Solo para usuarios no administradores
        Contribuyente.objects.create(users=instance)

@receiver(post_save, sender=User)
def guardar_perfil_contribuyente(sender, instance, **kwargs):
    if hasattr(instance, 'perfil_contribuyente'):
        instance.perfil_contribuyente.save()


    
class tram_planillas(models.Model):
    id = models.AutoField(primary_key=True)
    n_planilla = models.CharField(max_length=35, unique=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()


    class Meta:
        ordering = ['-id']
        db_table='tram_planillas'
    
    
class SolicitudTramite(models.Model):
    id = models.AutoField(primary_key=True)
    n_tramite = models.CharField(max_length=20, unique=True, blank=True)
    ESTADOS = (
        ('PENDIENTE', 'Pendiente de revisión'),
        ('REVISION', 'En revisión'),
        ('COMPLETADO', 'Completado'),
        ('RECHAZADO', 'Rechazado'),
        ('APROBADO', 'Aprobado'),
    )
    
    contribuyent = models.ForeignKey(Contribuyente, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)
    
    # Opción para cita presencial
    cita_presencial = models.DateTimeField(blank=True, null=True)
    asistio_cita = models.BooleanField(default=False)
    
    status = models.BooleanField()

    class Meta:
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Solicitud #{self.id} - ({self.estado})"
    
class HistorialTramite(models.Model):
    solicitud = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='historial')
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Contribuyente, on_delete=models.SET_NULL, null=True, blank=True)
    area_destino = models.CharField(max_length=100)  # O podrías crear un modelo Area si es más complejo
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    observaciones = models.TextField(blank=True, null=True)
    status = models.BooleanField()

    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Movimiento #{self.id} - {self.solicitud}"
    
class tram_solv_inm(models.Model):
    id = models.AutoField(primary_key=True)
    solicitud_inmu = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_solv_inm')
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_inm/',  blank=True)
    codigo_cast = models.CharField(max_length=20, unique=True, blank=True)
    codigo_sap = models.CharField(max_length=20, unique=True, blank=True)
    codigo_planilla = models.CharField(max_length=20)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    planilla_solicitud = models.FileField(upload_to ='planilla_inm/',  blank=True)

    tipo = (
        ('registro', 'Registro'),
        ('construcion', 'Construcción'),
        ('regist_hipo', 'Registro de Hipoteca'),
        ('posesion', 'Posesión'),
        ('remate', 'Remate'),
        ('solicit_arrend', 'Solicitud de Arriendamiento'),
        ('mensura', 'Mensura'),
        ('desocupacion', 'Desocupación'),
        ('internas', 'Internas'),
        ('tribut_espec', 'Tributaria Especial'),
        ('rural', 'Rural'),
        ('inti', 'INTI'),
        ('otros', 'otros'),
    )
    otros = models.CharField(max_length=100, blank=True, null=True)
    motivo = models.CharField(max_length=40, choices=tipo, null=False, blank=False, default='registro')
    planilla = models.ForeignKey(tram_planillas, on_delete=models.CASCADE, null=True, blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()

    class Meta:
        ordering = ['-id']
        db_table='tram_solv_inm'


class tram_solv_actecon(models.Model):
    idact = models.AutoField(primary_key=True)
    solicitud = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_solv_actecon')
    codigo_planilla = models.CharField(max_length=20)
    planilla_solicitud = models.FileField(upload_to ='planilla_actecono/',  blank=True)
    num_estampilla = models.CharField  (max_length=30)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_actecono/',  blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()
    status = models.BooleanField()

    class Meta:
        ordering = ['-idact']
        db_table='tram_solv_actecon'

class tram_solv_veh(models.Model):
    idvehi = models.AutoField(primary_key=True)
    solicitud_vehi = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_solv_veh')
    n_placa= models.CharField(max_length=20, unique=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    num_estampilla = models.CharField  (max_length=30)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_vehiculo/',  blank=True)
    codigo_planilla = models.CharField(max_length=20)
    planilla_solicitud = models.FileField(upload_to ='planilla_vehiculo/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()

    class Meta:
        ordering = ['-idvehi']
        db_table='tram_solv_veh'

class tram_solv_pub(models.Model):
    idpubli = models.AutoField(primary_key=True)
    solicitud_publi = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_solv_pub')
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField(null=True)
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_public/',  blank=True)
    cod_planilla = models.CharField(max_length=20, unique=True, blank=False)
    planilla_solicitud = models.FileField(upload_to='imagenPublicidad/', null=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()


    class Meta:
        ordering = ['-idpubli']
        db_table='tram_solv_pub'


class tram_cese_def(models.Model):
    idCe_def = models.AutoField(primary_key=True)
    solicitudCesedefi = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_cese_def')
    licencia = models.CharField(max_length=20, unique=True, blank=False)
    codigo_sap = models.CharField(max_length=20, unique=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_cese_def/',  blank=True)
    codigo_planilla = models.CharField(max_length=20, unique=True)
    planilla_solicitud = models.FileField(upload_to ='planilla_cese_def/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()

    class Meta:
        ordering = ['-idCe_def']
        db_table='tram_cese_def'


class tram_cese_temp(models.Model):
    idCe_temp = models.AutoField(primary_key=True)
    solicitudCesetemp = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_cese_temp')
    licencia = models.CharField(max_length=20, unique=True, blank=False)
    codigo_sap = models.CharField(max_length=20, unique=True, blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_cese_temp/',  blank=True)
    codigo_planilla = models.CharField(max_length=20)
    planilla_solicitud = models.FileField(upload_to ='planilla_cese_temp/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()

    class Meta:
        ordering = ['-idCe_temp']
        db_table='tram_cese_temp'

class pagos_pendientes_cesesdefitemp(models.Model):
    idpagocesedeftemp = models.AutoField(primary_key=True)
    num_tram_cese_temp = models.ForeignKey(tram_cese_temp, on_delete=models.CASCADE, related_name='pagos_pendientes_cesesdef')
    num_tram_cese_def = models.ForeignKey(tram_cese_def, on_delete=models.CASCADE, related_name='pagos_pendientes_cesesdef')
    tipo = (
        ('Cese_definitiva', 'Cese definitiva'),
        ('Cese_temporal', 'Cese_temporal'),
    )
    tipoCese = models.CharField(max_length=40, choices=tipo, blank=False, default='Cese_temporal')
    monto_total_pendiente = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    status = models.BooleanField()

class detalles_pagos_cesesdeftemp(models.Model):
    id = models.AutoField(primary_key=True)
    idpagocesedeftemp = models.ForeignKey(pagos_pendientes_cesesdefitemp, on_delete=models.CASCADE, related_name='detalles_pagos')
    Descripcion = models.CharField(max_length=255, null=False, blank=False)
    periodo_fiscal = models.CharField(max_length=50, blank=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    status = models.BooleanField()

class tram_const_exen(models.Model):
    id = models.AutoField(primary_key=True)
    solicitudexen = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_const_exen')
    codigo_sap = models.CharField(max_length=20, null=False, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    codigo_planilla = models.CharField(max_length=20)
    planilla_solicitud = models.FileField(upload_to ='planilla_const_exen/',  blank=True)
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_const_exen/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()

    class Meta:
        ordering = ['-id']
        db_table='tram_const_exen'

class tram_ivss_reg (models.Model):
    id = models.AutoField(primary_key=True)
    solicitud_ivssreg = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_ivss_reg')
    licencia = models.CharField(max_length=20, unique=True, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    planilla_solicitud = models.FileField(upload_to ='planilla_ivss_reg/',  blank=True)
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_ivss_reg/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()
    
    class Meta:
        ordering = ['-id']
        db_table='tram_ivss_reg'

class tram_ivss_noreg (models.Model):
    id = models.AutoField(primary_key=True)
    solicitud_ivssnoreg = models.ForeignKey(SolicitudTramite, on_delete=models.CASCADE, related_name='tram_ivss_noreg')
    licencia = models.CharField(max_length=20, unique=True, blank=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    planilla_solicitud = models.FileField(upload_to ='planilla_ivss_noreg/',  blank=True)
    n_estampilla = models.CharField(max_length=20, unique=True, blank=True)
    fecha_estampilla = models.DateField()
    Imagen_estampilla = models.FileField(upload_to ='Estampilla_ivss_noreg/',  blank=True)
    num_pago = models.CharField(max_length=20, unique=True, blank=False)
    fecha_pago = models.DateField()

    status = models.BooleanField()
   
    class Meta:
        ordering = ['-id']
        db_table='tram_ivss_noreg'


class Auditoria (models.Model):
    id = models.AutoField(primary_key=True)
    fechareg = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=250)
    estatus = models.BooleanField(default=True)
