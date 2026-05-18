from django.db import models
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Receta(models.Model):
    ESTADOS=[('emitida','Emitida'),('despachada','Despachada'),('cancelada','Cancelada')]
    paciente=models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name='recetas')
    veterinario=models.ForeignKey(Usuario,on_delete=models.PROTECT)
    consulta=models.ForeignKey('consultas.Consulta',on_delete=models.SET_NULL,null=True,blank=True)
    fecha_emision=models.DateField(auto_now_add=True)
    fecha_vencimiento=models.DateField(null=True,blank=True)
    estado=models.CharField(max_length=15,choices=ESTADOS,default='emitida')
    observaciones=models.TextField(blank=True)
    class Meta: verbose_name='Receta'; ordering=['-fecha_emision']
    def __str__(self): return f'Receta #{self.pk} – {self.paciente}'
class ItemReceta(models.Model):
    receta=models.ForeignKey(Receta,on_delete=models.CASCADE,related_name='items')
    producto=models.ForeignKey('inventario.Producto',on_delete=models.PROTECT)
    dosis=models.CharField(max_length=100)
    frecuencia=models.CharField(max_length=80)
    duracion=models.CharField(max_length=80)
    via=models.CharField(max_length=50)
    cantidad_despachar=models.DecimalField(max_digits=8,decimal_places=2,default=1)
    indicaciones=models.TextField(blank=True)
    despachado=models.BooleanField(default=False)
    def __str__(self): return f'{self.producto} – {self.dosis}'
