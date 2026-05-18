from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class TipoExamen(models.Model):
    nombre=models.CharField(max_length=100,unique=True)
    descripcion=models.TextField(blank=True)
    precio_ref=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    def __str__(self): return self.nombre
class Examen(models.Model):
    ESTADOS=[('solicitado','Solicitado'),('en_proceso','En proceso'),('completado','Completado'),('cancelado','Cancelado')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='examenes')
    tipo=models.ForeignKey(TipoExamen,on_delete=models.PROTECT)
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT,related_name='examenes_solicitados')
    fecha_solicitud=models.DateTimeField(auto_now_add=True)
    fecha_resultado=models.DateTimeField(null=True,blank=True)
    estado=models.CharField(max_length=15,choices=ESTADOS,default='solicitado')
    muestra=models.CharField(max_length=80,blank=True)
    resultado=models.TextField(blank=True)
    interpretacion=models.TextField(blank=True)
    archivo=models.FileField(upload_to='examenes/',blank=True,null=True)
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Examen'; verbose_name_plural='Exámenes'; ordering=['-fecha_solicitud']
    def __str__(self): return f'{self.tipo} – {self.paciente}'
