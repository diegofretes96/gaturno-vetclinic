from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Certificado(models.Model):
    TIPOS=[('salud','Certificado de salud'),('vacunas','Certificado de vacunas'),('viaje','Certificado de viaje'),('esterilizacion','Certificado de esterilización'),('defuncion','Certificado de defunción'),('otro','Otro')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='certificados')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    tipo=models.CharField(max_length=20,choices=TIPOS)
    fecha_emision=models.DateField(auto_now_add=True)
    fecha_vencimiento=models.DateField(null=True,blank=True)
    numero=models.CharField(max_length=20,unique=True,blank=True)
    contenido=models.TextField()
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Certificado'; verbose_name_plural='Certificados'; ordering=['-fecha_emision']
    def __str__(self): return f'{self.get_tipo_display()} – {self.paciente} ({self.numero})'
    def save(self,*a,**k):
        if not self.numero:
            from django.db.models import Max
            u=Certificado.objects.aggregate(m=Max('id'))['m'] or 0
            self.numero=f'CERT{str(u+1).zfill(5)}'
        super().save(*a,**k)
