from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Todas las URLs del sistema de gestión bajo /gestion-clinica/
gestion_patterns = [
    path('', include('apps.reportes.urls', namespace='reportes')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('propietarios/', include('apps.propietarios.urls', namespace='propietarios')),
    path('pacientes/', include('apps.pacientes.urls', namespace='pacientes')),
    path('agenda/', include('apps.agenda.urls', namespace='agenda')),
    path('consultas/', include('apps.consultas.urls', namespace='consultas')),
    path('vacunacion/', include('apps.vacunacion.urls', namespace='vacunacion')),
    path('desparasitacion/', include('apps.desparasitacion.urls', namespace='desparasitacion')),
    path('examenes/', include('apps.examenes.urls', namespace='examenes')),
    path('cirugia/', include('apps.cirugia.urls', namespace='cirugia')),
    path('hospitalizacion/', include('apps.hospitalizacion.urls', namespace='hospitalizacion')),
    path('farmacia/', include('apps.farmacia.urls', namespace='farmacia')),
    path('inventario/', include('apps.inventario.urls', namespace='inventario')),
    path('facturacion/', include('apps.facturacion.urls', namespace='facturacion')),
    path('estetica/', include('apps.estetica.urls', namespace='estetica')),
    path('certificados/', include('apps.certificados.urls', namespace='certificados')),
    path('vademecum/', include('apps.vademecum.urls', namespace='vademecum')),
]

urlpatterns = [
    # Panel de administración Django
    path('admin/', admin.site.urls),

    # Sitio web público (landing)
    path('', include('apps.landing.urls', namespace='landing')),

    # Sistema de gestión veterinaria
    path('gestion-clinica/', include(gestion_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
