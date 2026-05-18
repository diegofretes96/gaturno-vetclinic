from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Cirugia(models.Model):
    ESTADOS=[('programada','Programada'),('en_curso','En curso'),('completada','Completada'),('cancelada','Cancelada'),('complicacion','Con complicación')]
    ANESTESIA=[('local','Local'),('general_inh','General inhalatoria'),('general_iny','General inyectable'),('combinada','Combinada'),('ninguna','Sin anestesia')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='cirugias')
    cirujano=models.ForeignKey(Usuario,on_delete=models.PROTECT,related_name='cirugias')
    anestesista=models.ForeignKey(Usuario,on_delete=models.SET_NULL,null=True,blank=True,related_name='anestesias')
    fecha_programada=models.DateTimeField()
    fecha_inicio=models.DateTimeField(null=True,blank=True)
    fecha_fin=models.DateTimeField(null=True,blank=True)
    procedimiento=models.CharField(max_length=200)
    descripcion=models.TextField()
    tipo_anestesia=models.CharField(max_length=15,choices=ANESTESIA,default='general_inh')
    protocolo_anestesico=models.TextField(blank=True)
    hallazgos=models.TextField(blank=True)
    complicaciones=models.TextField(blank=True)
    estado=models.CharField(max_length=15,choices=ESTADOS,default='programada')
    cuidados_post=models.TextField(blank=True)
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Cirugía'; verbose_name_plural='Cirugías'; ordering=['-fecha_programada']
    def __str__(self): return f'{self.procedimiento} – {self.paciente}'
