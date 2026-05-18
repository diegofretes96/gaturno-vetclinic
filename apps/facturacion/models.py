from django.db import models
from django.utils import timezone
from django.db.models import Sum
from apps.propietarios.models import Propietario
from apps.pacientes.models import Paciente
from apps.accounts.models import Usuario
class Factura(models.Model):
    ESTADOS=[('borrador','Borrador'),('emitida','Emitida'),('pagada','Pagada'),('anulada','Anulada')]
    METODOS=[('efectivo','Efectivo'),('tarjeta_credito','Tarjeta crédito'),('tarjeta_debito','Tarjeta débito'),('transferencia','Transferencia'),('cheque','Cheque'),('mixto','Mixto')]
    numero=models.CharField(max_length=20,unique=True,blank=True)
    propietario=models.ForeignKey(Propietario,on_delete=models.PROTECT,related_name='facturas')
    paciente=models.ForeignKey(Paciente,on_delete=models.PROTECT,null=True,blank=True)
    fecha_emision=models.DateTimeField(default=timezone.now)
    estado=models.CharField(max_length=15,choices=ESTADOS,default='borrador')
    metodo_pago=models.CharField(max_length=20,choices=METODOS,blank=True)
    subtotal=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    descuento=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    iva=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    monto_pagado=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    observaciones=models.TextField(blank=True)
    creado_por=models.ForeignKey(Usuario,on_delete=models.SET_NULL,null=True)
    creado_en=models.DateTimeField(auto_now_add=True)
    class Meta: verbose_name='Factura'; verbose_name_plural='Facturas'; ordering=['-fecha_emision']
    def __str__(self): return f'Factura #{self.numero} – {self.propietario}'
    def save(self,*a,**k):
        if not self.numero:
            from django.db.models import Max
            u=Factura.objects.aggregate(m=Max('id'))['m'] or 0
            self.numero=f'F{str(u+1).zfill(6)}'
        super().save(*a,**k)
    def calcular_totales(self):
        from decimal import Decimal
        s=self.items.aggregate(s=Sum('subtotal'))['s'] or Decimal('0')
        self.subtotal=s;self.iva=round(s*Decimal('0.10'),2);self.total=s-self.descuento+self.iva
        self.save(update_fields=['subtotal','iva','total'])
    @property
    def saldo_pendiente(self): return self.total-self.monto_pagado
class ItemFactura(models.Model):
    factura=models.ForeignKey(Factura,on_delete=models.CASCADE,related_name='items')
    descripcion=models.CharField(max_length=200)
    producto=models.ForeignKey('inventario.Producto',on_delete=models.SET_NULL,null=True,blank=True)
    cantidad=models.DecimalField(max_digits=8,decimal_places=2,default=1)
    precio_unitario=models.DecimalField(max_digits=12,decimal_places=2)
    descuento_item=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    subtotal=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    def save(self,*a,**k):
        self.subtotal=(self.cantidad*self.precio_unitario)-self.descuento_item;super().save(*a,**k)
    def __str__(self): return f'{self.descripcion} x{self.cantidad}'
