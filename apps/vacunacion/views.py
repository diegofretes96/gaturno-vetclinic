from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .models import Vacunacion,Vacuna
from .forms import VacunacionForm,VacunaForm
@login_required
def lista(request):
    qs=Vacunacion.objects.select_related('paciente','vacuna','veterinario').order_by('-fecha_aplicacion')
    proximas=Vacunacion.objects.filter(proxima_dosis__gte=timezone.now().date(),proxima_dosis__lte=timezone.now().date()+timedelta(days=30)).select_related('paciente','vacuna').order_by('proxima_dosis')[:10]
    return render(request,'vacunacion/lista.html',{'vacunaciones':Paginator(qs,25).get_page(request.GET.get('page')),'proximas':proximas})
@login_required
def detalle(request,pk): return render(request,'vacunacion/detalle.html',{'obj':get_object_or_404(Vacunacion,pk=pk)})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=VacunacionForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Vacunación registrada.');return redirect('vacunacion:detalle',pk=obj.pk)
    return render(request,'vacunacion/form.html',{'form':form,'titulo':'Registrar vacunación'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Vacunacion,pk=pk)
    form=VacunacionForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('vacunacion:detalle',pk=obj.pk)
    return render(request,'vacunacion/form.html',{'form':form,'titulo':'Editar vacunación','obj':obj})
@login_required
def lista_vacunas(request): return render(request,'vacunacion/vacunas.html',{'vacunas':Vacuna.objects.select_related('especie').all()})
@login_required
def crear_vacuna(request):
    form=VacunaForm(request.POST or None)
    if form.is_valid():
        form.save();messages.success(request,'Vacuna creada.');return redirect('vacunacion:vacunas')
    return render(request,'vacunacion/form_vacuna.html',{'form':form,'titulo':'Nueva vacuna'})
