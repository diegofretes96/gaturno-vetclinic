from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Estetica(models.Model):
    SERVICIOS=[('bano','Baño'),('corte','Corte'),('bano_corte','Baño y corte'),('guarderia','Guardería'),('completo','Servicio completo')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='servicios_estetica')
    esteticista=models.ForeignKey(Usuario,on_delete=models.PROTECT,related_name='servicios_estetica')
    servicio=models.CharField(max_length=20,choices=SERVICIOS)
    fecha=models.DateTimeField()
    duracion_horas=models.PositiveSmallIntegerField(default=2)
    precio=models.DecimalField(max_digits=12,decimal_places=2)
    observaciones=models.TextField(blank=True)
    foto_antes=models.ImageField(upload_to='estetica/',blank=True,null=True)
    foto_despues=models.ImageField(upload_to='estetica/',blank=True,null=True)
    completado=models.BooleanField(default=False)
    class Meta: verbose_name='Servicio estético'; verbose_name_plural='Servicios estéticos'; ordering=['-fecha']
    def __str__(self): return f'{self.get_servicio_display()} – {self.paciente}'
