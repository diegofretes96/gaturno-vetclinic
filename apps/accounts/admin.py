from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display=['username','nombre_completo','email','rol']
    list_filter=['rol']
    fieldsets=UserAdmin.fieldsets+(('Clínica',{'fields':('rol','telefono','matricula','especialidad','foto')}),)
