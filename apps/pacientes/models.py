from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from apps.propietarios.models import Propietario

class Especie(models.Model):
    nombre=models.CharField(max_length=50,unique=True)
    icono=models.CharField(max_length=10,default='🐾')
    def __str__(self): return self.nombre

class Raza(models.Model):
    especie=models.ForeignKey(Especie,on_delete=models.CASCADE,related_name='razas')
    nombre=models.CharField(max_length=80)
    class Meta: ordering=['nombre']; unique_together=['especie','nombre']
    def __str__(self): return self.nombre

class Paciente(models.Model):
    SEXO=[('M','Macho'),('H','Hembra')]
    ESTADO=[('activo','Activo'),('fallecido','Fallecido'),('dado_baja','Dado de baja')]
    propietario=models.ForeignKey(Propietario,on_delete=models.CASCADE,related_name='mascotas')
    nombre=models.CharField(max_length=80)
    especie=models.ForeignKey(Especie,on_delete=models.PROTECT)
    raza=models.ForeignKey(Raza,on_delete=models.SET_NULL,null=True,blank=True)
    sexo=models.CharField(max_length=1,choices=SEXO)
    fecha_nacimiento=models.DateField(null=True,blank=True)
    color=models.CharField(max_length=60,blank=True)
    peso=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    microchip=models.CharField(max_length=50,blank=True,null=True,unique=True)
    esterilizado=models.BooleanField(default=False)
    foto=models.ImageField(upload_to='pacientes/',blank=True,null=True)
    alergias=models.TextField(blank=True)
    antecedentes=models.TextField(blank=True)
    estado=models.CharField(max_length=15,choices=ESTADO,default='activo')
    fecha_registro=models.DateTimeField(auto_now_add=True)
    history=HistoricalRecords()
    class Meta: verbose_name='Paciente'; verbose_name_plural='Pacientes'; ordering=['nombre']
    def __str__(self): return f'{self.nombre} ({self.propietario.apellidos})'
    @property
    def edad(self):
        if not self.fecha_nacimiento: return 'Desconocida'
        delta=timezone.now().date()-self.fecha_nacimiento
        a=delta.days//365; m=(delta.days%365)//30
        return f'{a}a {m}m' if a>0 else f'{m} mes{"es" if m!=1 else ""}'
    @property
    def emoji(self):
        n=self.especie.nombre.lower()
        return '😺' if 'gat' in n else '🐶' if ('perr' in n or 'can' in n) else self.especie.icono
