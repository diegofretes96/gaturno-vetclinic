from django.contrib import admin
from .models import Consulta,NotaClinica,Prescripcion
class RxInline(admin.TabularInline):
    model=Prescripcion;extra=0
class NInline(admin.TabularInline):
    model=NotaClinica;extra=0
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display=['paciente','veterinario','tipo','fecha','diagnostico_definitivo']
    inlines=[RxInline,NInline]
    search_fields=['paciente__nombre']
