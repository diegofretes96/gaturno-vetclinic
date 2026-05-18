from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Desparasitacion(models.Model):
    TIPO=[('interna','Interna'),('externa','Externa'),('ambas','Interna y externa')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='desparasitaciones')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    tipo=models.CharField(max_length=10,choices=TIPO)
    producto_nombre=models.CharField(max_length=100)
    dosis=models.CharField(max_length=80)
    fecha_aplicacion=models.DateField()
    proxima_aplicacion=models.DateField(null=True,blank=True)
    peso_momento=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Desparasitación'; verbose_name_plural='Desparasitaciones'; ordering=['-fecha_aplicacion']
    def __str__(self): return f'{self.get_tipo_display()} – {self.paciente} ({self.fecha_aplicacion})'
