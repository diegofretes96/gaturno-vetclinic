from django.contrib import admin
from .models import Propietario
@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display=['apellidos','nombres','numero_documento','telefono','total_mascotas','activo']
    list_filter=['activo','tipo_documento']
    search_fields=['nombres','apellidos','numero_documento']
