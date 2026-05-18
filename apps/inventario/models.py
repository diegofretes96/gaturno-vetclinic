from django.db import models
from django.utils import timezone
class Categoria(models.Model):
    nombre=models.CharField(max_length=80,unique=True)
    descripcion=models.CharField(max_length=200,blank=True)
    def __str__(self): return self.nombre
class Proveedor(models.Model):
    nombre=models.CharField(max_length=150);ruc=models.CharField(max_length=20,blank=True)
    telefono=models.CharField(max_length=20,blank=True);email=models.EmailField(blank=True)
    direccion=models.TextField(blank=True);contacto=models.CharField(max_length=100,blank=True)
    activo=models.BooleanField(default=True)
    class Meta: verbose_name_plural='Proveedores'
    def __str__(self): return self.nombre
class Producto(models.Model):
    TIPOS=[('medicamento','Medicamento'),('insumo','Insumo médico'),('alimento','Alimento'),('accesorio','Accesorio'),('cosmetico','Cosmético'),('vacuna','Vacuna'),('otro','Otro')]
    codigo=models.CharField(max_length=30,unique=True)
    nombre=models.CharField(max_length=150)
    nombre_generico=models.CharField(max_length=150,blank=True)
    tipo=models.CharField(max_length=20,choices=TIPOS,default='insumo')
    categoria=models.ForeignKey(Categoria,on_delete=models.SET_NULL,null=True,blank=True)
    proveedor=models.ForeignKey(Proveedor,on_delete=models.SET_NULL,null=True,blank=True)
    unidad_medida=models.CharField(max_length=30)
    precio_costo=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    precio_venta=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    stock_actual=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    stock_minimo=models.DecimalField(max_digits=10,decimal_places=2,default=5)
    requiere_receta=models.BooleanField(default=False)
    descripcion=models.TextField(blank=True)
    activo=models.BooleanField(default=True)
    class Meta: verbose_name='Producto'; verbose_name_plural='Productos'; ordering=['nombre']
    def __str__(self): return f'{self.nombre} ({self.codigo})'
    @property
    def bajo_stock(self): return self.stock_actual<=self.stock_minimo
class MovimientoStock(models.Model):
    TIPOS=[('entrada','Entrada'),('salida','Salida'),('ajuste','Ajuste'),('vencimiento','Baja por vencimiento')]
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE,related_name='movimientos')
    tipo=models.CharField(max_length=15,choices=TIPOS)
    cantidad=models.DecimalField(max_digits=10,decimal_places=2)
    stock_anterior=models.DecimalField(max_digits=10,decimal_places=2)
    stock_resultante=models.DecimalField(max_digits=10,decimal_places=2)
    motivo=models.CharField(max_length=200,blank=True)
    fecha=models.DateTimeField(default=timezone.now)
    usuario=models.ForeignKey('accounts.Usuario',on_delete=models.SET_NULL,null=True)
    class Meta: ordering=['-fecha']
    def __str__(self): return f'{self.get_tipo_display()} {self.cantidad} – {self.producto}'
