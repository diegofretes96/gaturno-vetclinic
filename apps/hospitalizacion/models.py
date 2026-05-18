from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Habitacion(models.Model):
    TIPOS=[('general','General'),('uci','UCI'),('postoperatorio','Postoperatorio'),('aislamiento','Aislamiento')]
    numero=models.CharField(max_length=10,unique=True)
    tipo=models.CharField(max_length=20,choices=TIPOS,default='general')
    capacidad=models.PositiveSmallIntegerField(default=1)
    descripcion=models.CharField(max_length=150,blank=True)
    activo=models.BooleanField(default=True)
    class Meta: verbose_name='Habitación'; verbose_name_plural='Habitaciones'
    def __str__(self): return f'Hab. {self.numero} ({self.get_tipo_display()})'
    @property
    def disponible(self): return self.internamientos.filter(estado='internado').count()<self.capacidad
class Internamiento(models.Model):
    ESTADOS=[('internado','Internado'),('alta_medica','Alta médica'),('fallecido','Fallecido'),('alta_voluntaria','Alta voluntaria')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='internamientos')
    habitacion=models.ForeignKey(Habitacion,on_delete=models.PROTECT,related_name='internamientos')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha_ingreso=models.DateTimeField(default=timezone.now)
    fecha_alta=models.DateTimeField(null=True,blank=True)
    motivo_ingreso=models.TextField()
    diagnostico_ingreso=models.TextField(blank=True)
    estado=models.CharField(max_length=20,choices=ESTADOS,default='internado')
    dieta=models.TextField(blank=True)
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Internamiento'; verbose_name_plural='Internamientos'; ordering=['-fecha_ingreso']
    def __str__(self): return f'{self.paciente} – Hab.{self.habitacion.numero}'
    @property
    def dias_internado(self):
        fin=self.fecha_alta or timezone.now()
        return max((fin-self.fecha_ingreso).days,0)
class EvolucionDiaria(models.Model):
    internamiento=models.ForeignKey(Internamiento,on_delete=models.CASCADE,related_name='evoluciones')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha=models.DateTimeField(auto_now_add=True)
    peso=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    temperatura=models.DecimalField(max_digits=4,decimal_places=1,null=True,blank=True)
    fc=models.PositiveSmallIntegerField(null=True,blank=True)
    fr=models.PositiveSmallIntegerField(null=True,blank=True)
    estado_general=models.CharField(max_length=50,blank=True)
    alimentacion=models.CharField(max_length=80,blank=True)
    descripcion=models.TextField()
    plan=models.TextField(blank=True)
    class Meta: ordering=['-fecha']
    def __str__(self): return f'Evolución {self.fecha.strftime("%d/%m/%Y %H:%M")}'
