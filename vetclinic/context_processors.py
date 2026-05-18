from django.conf import settings

def clinica_config(request):
    ctx = {
        'CLINICA_NOMBRE': settings.CLINICA_NOMBRE,
        'CLINICA_DIRECCION': getattr(settings, 'CLINICA_DIRECCION', ''),
        'CLINICA_TELEFONO': getattr(settings, 'CLINICA_TELEFONO', ''),
        'MONEDA_SIMBOLO': getattr(settings, 'MONEDA_SIMBOLO', 'Gs.'),
    }
    if request.user.is_authenticated:
        from django.utils import timezone
        try:
            from apps.agenda.models import Cita
            ctx['citas_hoy_count'] = Cita.objects.filter(
                fecha__date=timezone.now().date(), estado__in=['pendiente','confirmada']).count()
        except: ctx['citas_hoy_count'] = 0
        try:
            from apps.hospitalizacion.models import Internamiento
            ctx['internados_count'] = Internamiento.objects.filter(estado='internado').count()
        except: ctx['internados_count'] = 0
        try:
            from apps.pacientes.models import Paciente
            ctx['total_pacientes'] = Paciente.objects.filter(estado='activo').count()
        except: ctx['total_pacientes'] = 0
    return ctx
