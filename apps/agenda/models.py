from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario

class Cita(models.Model):
    ESTADOS=[('pendiente','Pendiente'),('confirmada','Confirmada'),('en_consulta','En consulta'),
             ('realizada','Realizada'),('cancelada','Cancelada'),('no_asistio','No asistió')]
    TIPOS=[('consulta','Consulta médica'),('control','Control'),('vacunacion','Vacunación'),
           ('desparasitacion','Desparasitación'),('cirugia','Cirugía'),('examenes','Exámenes'),
           ('bano_corte','Baño y corte'),('guarderia','Guardería'),('otro','Otro')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='citas')
    veterinario=models.ForeignKey(Usuario,on_delete=models.SET_NULL,null=True,blank=True,related_name='citas')
    tipo=models.CharField(max_length=20,choices=TIPOS,default='consulta')
    fecha=models.DateTimeField()
    duracion_min=models.PositiveIntegerField(default=30)
    motivo=models.TextField()
    notas=models.TextField(blank=True)
    estado=models.CharField(max_length=15,choices=ESTADOS,default='pendiente')
    creado_en=models.DateTimeField(auto_now_add=True)
    creado_por=models.ForeignKey(Usuario,on_delete=models.SET_NULL,null=True,related_name='citas_creadas')
    class Meta: verbose_name='Cita'; verbose_name_plural='Citas'; ordering=['fecha']
    def __str__(self): return f'{self.paciente} – {self.fecha.strftime("%d/%m/%Y %H:%M")}'
    @property
    def es_hoy(self): return self.fecha.date()==timezone.now().date()

class SalaEspera(models.Model):
    cita=models.OneToOneField(Cita,on_delete=models.CASCADE,related_name='espera')
    hora_llegada=models.DateTimeField(auto_now_add=True)
    hora_atencion=models.DateTimeField(null=True,blank=True)
    prioridad=models.PositiveSmallIntegerField(default=5)
    notas_recepcion=models.TextField(blank=True)
    class Meta: ordering=['prioridad','hora_llegada']
    def __str__(self): return f'Espera: {self.cita.paciente}'
    @property
    def tiempo_espera_min(self): return int((timezone.now()-self.hora_llegada).total_seconds()/60)
