from django.db import models
from simple_history.models import HistoricalRecords

class Propietario(models.Model):
    TIPO_DOC=[('ci','Cédula'),('ruc','RUC'),('pasaporte','Pasaporte')]
    nombres=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    tipo_documento=models.CharField(max_length=15,choices=TIPO_DOC,default='ci',blank=True)
    numero_documento=models.CharField(max_length=20,unique=True,blank=True,null=True)
    telefono=models.CharField(max_length=20)
    telefono_alt=models.CharField(max_length=20,blank=True)
    email=models.EmailField(blank=True)
    direccion=models.TextField(blank=True)
    ciudad=models.CharField(max_length=80,blank=True)
    fecha_nacimiento=models.DateField(null=True,blank=True)
    observaciones=models.TextField(blank=True)
    fecha_registro=models.DateTimeField(auto_now_add=True)
    activo=models.BooleanField(default=True)
    history=HistoricalRecords()
    class Meta:
        verbose_name='Propietario';verbose_name_plural='Propietarios';ordering=['apellidos','nombres']
    def __str__(self): return f'{self.apellidos}, {self.nombres}'
    @property
    def nombre_completo(self): return f'{self.nombres} {self.apellidos}'
    @property
    def total_mascotas(self): return self.mascotas.filter(estado='activo').count()


class DatosFacturacion(models.Model):
    propietario=models.OneToOneField(
        Propietario,on_delete=models.CASCADE,related_name='datos_facturacion'
    )
    razon_social=models.CharField(max_length=200,verbose_name='Razón Social / Nombre')
    ruc=models.CharField(max_length=20,verbose_name='RUC')
    class Meta:
        verbose_name='Datos de Facturación'
        verbose_name_plural='Datos de Facturación'
    def __str__(self): return f'{self.razon_social} – {self.ruc}'
