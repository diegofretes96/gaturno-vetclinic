from django.db import models
from apps.pacientes.models import Paciente,Especie
from apps.accounts.models import Usuario
class Vacuna(models.Model):
    nombre=models.CharField(max_length=100)
    fabricante=models.CharField(max_length=100,blank=True)
    especie=models.ForeignKey(Especie,on_delete=models.PROTECT)
    intervalo_dias=models.PositiveIntegerField(default=365)
    descripcion=models.TextField(blank=True)
    activo=models.BooleanField(default=True)
    class Meta: ordering=['nombre']
    def __str__(self): return f'{self.nombre} ({self.especie})'
class Vacunacion(models.Model):
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='vacunaciones')
    vacuna=models.ForeignKey(Vacuna,on_delete=models.PROTECT)
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha_aplicacion=models.DateField()
    lote=models.CharField(max_length=50,blank=True)
    dosis=models.CharField(max_length=30,blank=True)
    via=models.CharField(max_length=50,blank=True)
    sitio=models.CharField(max_length=80,blank=True)
    proxima_dosis=models.DateField(null=True,blank=True)
    observaciones=models.TextField(blank=True)
    creado_en=models.DateTimeField(auto_now_add=True)
    class Meta: verbose_name='Vacunación'; verbose_name_plural='Vacunaciones'; ordering=['-fecha_aplicacion']
    def __str__(self): return f'{self.vacuna} – {self.paciente} ({self.fecha_aplicacion})'
    def save(self,*a,**k):
        if not self.proxima_dosis and self.vacuna.intervalo_dias:
            from datetime import timedelta
            self.proxima_dosis=self.fecha_aplicacion+timedelta(days=self.vacuna.intervalo_dias)
        super().save(*a,**k)
