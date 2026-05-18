from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Cita,SalaEspera
from .forms import CitaForm,SalaEsperaForm
CMAP={'consulta':'#1D9E75','vacunacion':'#EF9F27','cirugia':'#D85A30','examenes':'#7F77DD','bano_corte':'#639922','desparasitacion':'#D4537E','control':'#378ADD'}

@login_required
def lista(request):
    qs=Cita.objects.select_related('paciente','veterinario').order_by('-fecha')
    estado=request.GET.get('estado','')
    if estado: qs=qs.filter(estado=estado)
    return render(request,'agenda/lista.html',{'citas':Paginator(qs,25).get_page(request.GET.get('page')),'estado_sel':estado,'estados':Cita.ESTADOS})

@login_required
def calendario(request):
    from apps.accounts.models import Usuario
    return render(request,'agenda/calendario.html',{'veterinarios':Usuario.objects.filter(rol__in=['veterinario','admin'])})

@login_required
def citas_json(request):
    qs=Cita.objects.exclude(estado='cancelada').select_related('paciente')
    return JsonResponse([{'id':c.pk,'title':f'{c.paciente.nombre} – {c.get_tipo_display()}','start':c.fecha.isoformat(),'color':CMAP.get(c.tipo,'#378ADD')} for c in qs],safe=False)

@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    form=CitaForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save(commit=False);obj.creado_por=request.user;obj.save()
        messages.success(request,'Cita agendada.');return redirect('agenda:lista')
    return render(request,'agenda/form.html',{'form':form,'titulo':'Nueva cita'})

@login_required
def editar(request,pk):
    obj=get_object_or_404(Cita,pk=pk)
    form=CitaForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('agenda:lista')
    return render(request,'agenda/form.html',{'form':form,'titulo':'Editar cita','obj':obj})

@login_required
def cancelar(request,pk):
    obj=get_object_or_404(Cita,pk=pk);obj.estado='cancelada';obj.save()
    messages.success(request,'Cita cancelada.');return redirect('agenda:lista')

@login_required
def sala_espera(request):
    hoy=timezone.now().date()
    sala=SalaEspera.objects.filter(cita__fecha__date=hoy,hora_atencion__isnull=True).select_related('cita__paciente__especie','cita__paciente__propietario','cita__veterinario')
    return render(request,'agenda/sala_espera.html',{'sala':sala})

@login_required
def agregar_sala(request):
    form=SalaEsperaForm(request.POST or None)
    if form.is_valid():
        form.save();messages.success(request,'Agregado a sala de espera.');return redirect('agenda:sala_espera')
    return render(request,'agenda/form_sala.html',{'form':form,'titulo':'Agregar a sala de espera'})

@login_required
def atender(request,pk):
    espera=get_object_or_404(SalaEspera,pk=pk)
    espera.hora_atencion=timezone.now();espera.save()
    espera.cita.estado='en_consulta';espera.cita.save()
    return redirect('consultas:nueva_cita',pk=espera.cita.pk)

def sala_count(request):
    count=SalaEspera.objects.filter(cita__fecha__date=timezone.now().date(),hora_atencion__isnull=True).count()
    return JsonResponse({'count':count})
