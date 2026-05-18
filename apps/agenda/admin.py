from django.contrib import admin
from .models import Cita,SalaEspera
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display=['paciente','veterinario','tipo','fecha','estado']
    list_filter=['tipo','estado']
    search_fields=['paciente__nombre']
admin.site.register(SalaEspera)
