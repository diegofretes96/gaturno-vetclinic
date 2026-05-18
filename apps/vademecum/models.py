from django.db import models
from apps.pacientes.models import Especie
class Medicamento(models.Model):
    nombre_comercial=models.CharField(max_length=150)
    nombre_generico=models.CharField(max_length=150,blank=True)
    principio_activo=models.CharField(max_length=200,blank=True)
    concentracion=models.CharField(max_length=80,blank=True)
    forma_farmaceutica=models.CharField(max_length=80,blank=True)
    laboratorio=models.CharField(max_length=100,blank=True)
    indicaciones=models.TextField(blank=True)
    contraindicaciones=models.TextField(blank=True)
    dosis_recomendada=models.TextField(blank=True)
    via_administracion=models.CharField(max_length=80,blank=True)
    especies=models.ManyToManyField(Especie,blank=True)
    requiere_receta=models.BooleanField(default=False)
    activo=models.BooleanField(default=True)
    class Meta: verbose_name='Medicamento'; verbose_name_plural='Medicamentos'; ordering=['nombre_comercial']
    def __str__(self): return f'{self.nombre_comercial} {self.concentracion}'
