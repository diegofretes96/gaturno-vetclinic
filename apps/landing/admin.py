from django.contrib import admin
from .models import ConfigSite, GaleriaFoto, ProductoWeb


@admin.register(ConfigSite)
class ConfigSiteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos de la clínica', {
            'fields': ('nombre_clinica', 'slogan', 'texto_hero')
        }),
        ('Contacto y ubicación', {
            'fields': ('direccion', 'horario', 'telefono', 'whatsapp', 'email_contacto')
        }),
        ('Redes sociales', {
            'fields': ('instagram', 'facebook')
        }),
        ('Google Maps', {
            'fields': ('google_maps_embed',),
            'description': 'En Google Maps → Compartir → Incorporar mapa → copiá solo el valor del atributo src="..."'
        }),
    )

    def has_add_permission(self, request):
        # Solo permite una fila (singleton)
        return not ConfigSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GaleriaFoto)
class GaleriaFotoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activo']
    list_editable = ['orden', 'activo']
    list_filter = ['activo']
    ordering = ['orden']


@admin.register(ProductoWeb)
class ProductoWebAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'disponible', 'orden']
    list_editable = ['precio', 'disponible', 'orden']
    list_filter = ['disponible']
    search_fields = ['nombre']
    ordering = ['orden', 'nombre']
