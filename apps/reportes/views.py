from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum,Count
from datetime import timedelta
@login_required
def dashboard(request):
    from apps.agenda.models import Cita,SalaEspera
    from apps.pacientes.models import Paciente
    from apps.propietarios.models import Propietario
    from apps.hospitalizacion.models import Internamiento
    from apps.facturacion.models import Factura
    from apps.vacunacion.models import Vacunacion
    hoy=timezone.now().date(); inicio_mes=hoy.replace(day=1)
    sala_espera=SalaEspera.objects.filter(cita__fecha__date=hoy,hora_atencion__isnull=True).select_related('cita__paciente__especie','cita__paciente__propietario','cita__veterinario').order_by('prioridad','hora_llegada')
    citas_hoy=Cita.objects.filter(fecha__date=hoy).exclude(estado='cancelada').select_related('paciente__especie','veterinario').order_by('fecha')
    internados=Internamiento.objects.filter(estado='internado').select_related('paciente','habitacion','veterinario')
    ingresos_hoy=Factura.objects.filter(fecha_emision__date=hoy,estado='pagada').aggregate(t=Sum('total'))['t'] or 0
    ingresos_semana=Factura.objects.filter(fecha_emision__date__gte=hoy-timedelta(days=7),estado='pagada').aggregate(t=Sum('total'))['t'] or 0
    proximos_cumples=[]
    for p in Paciente.objects.filter(estado='activo',fecha_nacimiento__isnull=False).select_related('propietario')[:300]:
        try:
            cumple=p.fecha_nacimiento.replace(year=hoy.year)
            if cumple<hoy: cumple=cumple.replace(year=hoy.year+1)
            dias=(cumple-hoy).days
            if 0<=dias<=7: proximos_cumples.append({'paciente':p,'dias':dias,'fecha':cumple})
        except: pass
    proximos_cumples.sort(key=lambda x:x['dias'])
    vacunas_proximas=Vacunacion.objects.filter(proxima_dosis__gte=hoy,proxima_dosis__lte=hoy+timedelta(days=15)).select_related('paciente__propietario','vacuna').order_by('proxima_dosis')[:10]
    return render(request,'base/dashboard.html',{
        'sala_espera':sala_espera,'citas_hoy':citas_hoy,'internados':internados,'internados_count':internados.count(),
        'ingresos_hoy':ingresos_hoy,'ingresos_semana':ingresos_semana,
        'pacientes_hoy':Cita.objects.filter(fecha__date=hoy,estado__in=['realizada','en_consulta']).count(),
        'proximos_cumples':proximos_cumples[:5],'vacunas_proximas':vacunas_proximas,
        'total_pacientes':Paciente.objects.filter(estado='activo').count(),
        'total_propietarios':Propietario.objects.filter(activo=True).count(),
        'consultas_mes':Cita.objects.filter(fecha__date__gte=inicio_mes,estado='realizada').count(),
        'fecha_hoy':hoy,
    })
@login_required
def reportes_index(request):
    from apps.facturacion.models import Factura
    from apps.consultas.models import Consulta
    from apps.pacientes.models import Paciente
    from apps.agenda.models import Cita
    hoy=timezone.now().date(); inicio_mes=hoy.replace(day=1)
    return render(request,'reportes/index.html',{
        'ingresos_mes':Factura.objects.filter(fecha_emision__date__gte=inicio_mes,estado='pagada').aggregate(t=Sum('total'))['t'] or 0,
        'consultas_mes':Consulta.objects.filter(fecha__month=hoy.month,fecha__year=hoy.year).count(),
        'pacientes_nuevos_mes':Paciente.objects.filter(fecha_registro__month=hoy.month,fecha_registro__year=hoy.year).count(),
        'top_servicios':list(Cita.objects.filter(fecha__month=hoy.month).values('tipo').annotate(total=Count('id')).order_by('-total')[:6]),
    })
