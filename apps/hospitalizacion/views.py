from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Internamiento,EvolucionDiaria,Habitacion
from .forms import InternamientoForm,EvolucionForm
@login_required
def lista(request):
    internados=Internamiento.objects.filter(estado='internado').select_related('paciente','habitacion','veterinario')
    historial=Internamiento.objects.exclude(estado='internado').select_related('paciente','habitacion').order_by('-fecha_ingreso')
    return render(request,'hospitalizacion/lista.html',{'internados':internados,'historial':Paginator(historial,20).get_page(request.GET.get('page')),'habitaciones':Habitacion.objects.filter(activo=True)})
@login_required
def detalle(request,pk):
    obj=get_object_or_404(Internamiento.objects.select_related('paciente','habitacion','veterinario'),pk=pk)
    form=EvolucionForm(initial={'veterinario':request.user.pk} if request.user.es_veterinario else {})
    return render(request,'hospitalizacion/detalle.html',{'obj':obj,'form':form,'evoluciones':obj.evoluciones.select_related('veterinario').order_by('-fecha')})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=InternamientoForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Internamiento registrado.');return redirect('hospitalizacion:detalle',pk=obj.pk)
    return render(request,'hospitalizacion/form.html',{'form':form,'titulo':'Nuevo internamiento'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Internamiento,pk=pk)
    form=InternamientoForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('hospitalizacion:detalle',pk=obj.pk)
    return render(request,'hospitalizacion/form.html',{'form':form,'titulo':'Editar internamiento','obj':obj})
@login_required
def evolucion(request,pk):
    obj=get_object_or_404(Internamiento,pk=pk)
    form=EvolucionForm(request.POST or None)
    if form.is_valid():
        ev=form.save(commit=False);ev.internamiento=obj;ev.save()
        messages.success(request,'Evolución registrada.');return redirect('hospitalizacion:detalle',pk=pk)
    return render(request,'hospitalizacion/form_evolucion.html',{'form':form,'obj':obj,'titulo':'Nueva evolución'})
@login_required
def alta(request,pk):
    obj=get_object_or_404(Internamiento,pk=pk)
    if request.method=='POST':
        obj.estado=request.POST.get('estado','alta_medica');obj.fecha_alta=timezone.now();obj.save()
        messages.success(request,'Alta registrada.');return redirect('hospitalizacion:lista')
    return render(request,'hospitalizacion/alta.html',{'obj':obj})
