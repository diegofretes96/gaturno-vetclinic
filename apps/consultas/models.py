from django.db import models
from simple_history.models import HistoricalRecords
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario

class Consulta(models.Model):
    TIPOS=[('primera_vez','Primera vez'),('control','Control'),('urgencia','Urgencia'),('posoperatorio','Postoperatorio'),('virtual','Virtual')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='consultas')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT,related_name='consultas')
    cita=models.OneToOneField('agenda.Cita',on_delete=models.SET_NULL,null=True,blank=True)
    tipo=models.CharField(max_length=20,choices=TIPOS,default='primera_vez')
    fecha=models.DateTimeField(auto_now_add=True)
    motivo_consulta=models.TextField()
    anamnesis=models.TextField(blank=True)
    peso=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    temperatura=models.DecimalField(max_digits=4,decimal_places=1,null=True,blank=True)
    fc=models.PositiveSmallIntegerField(null=True,blank=True,verbose_name='FC (lpm)')
    fr=models.PositiveSmallIntegerField(null=True,blank=True,verbose_name='FR (rpm)')
    mucosas=models.CharField(max_length=50,blank=True)
    linfonodos=models.CharField(max_length=100,blank=True)
    condicion_corporal=models.PositiveSmallIntegerField(null=True,blank=True,help_text='1-9')
    subjetivo=models.TextField(blank=True)
    objetivo=models.TextField(blank=True)
    evaluacion=models.TextField(blank=True)
    plan=models.TextField(blank=True)
    diagnostico_presuntivo=models.TextField(blank=True)
    diagnostico_definitivo=models.TextField(blank=True)
    pronostico=models.CharField(max_length=50,blank=True)
    observaciones=models.TextField(blank=True)
    proxima_cita=models.DateField(null=True,blank=True)
    history=HistoricalRecords()
    class Meta: verbose_name='Consulta'; verbose_name_plural='Consultas'; ordering=['-fecha']
    def __str__(self): return f'Consulta #{self.pk} – {self.paciente} ({self.fecha.strftime("%d/%m/%Y")})'

class NotaClinica(models.Model):
    consulta=models.ForeignKey(Consulta,on_delete=models.CASCADE,related_name='notas')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha=models.DateTimeField(auto_now_add=True)
    nota=models.TextField()
    class Meta: ordering=['-fecha']

class Prescripcion(models.Model):
    consulta=models.ForeignKey(Consulta,on_delete=models.CASCADE,related_name='prescripciones')
    medicamento_nombre=models.CharField(max_length=150)
    dosis=models.CharField(max_length=100)
    frecuencia=models.CharField(max_length=80)
    duracion=models.CharField(max_length=80)
    via=models.CharField(max_length=50)
    indicaciones=models.TextField(blank=True)
    def __str__(self): return f'{self.medicamento_nombre}'
