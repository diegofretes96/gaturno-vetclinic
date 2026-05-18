from django.contrib import admin
from .models import Categoria,Proveedor,Producto,MovimientoStock
admin.site.register(Categoria);admin.site.register(Proveedor)
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display=['nombre','codigo','tipo','stock_actual','stock_minimo','precio_venta','activo']
    list_filter=['tipo','activo','categoria']
    search_fields=['nombre','codigo']
admin.site.register(MovimientoStock)
