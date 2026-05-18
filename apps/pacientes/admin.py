from django.contrib import admin
from .models import Especie,Raza,Paciente
admin.site.register(Especie); admin.site.register(Raza)
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display=['nombre','especie','raza','propietario','sexo','esterilizado','estado']
    list_filter=['especie','sexo','esterilizado','estado']
    search_fields=['nombre','microchip','propietario__apellidos']
