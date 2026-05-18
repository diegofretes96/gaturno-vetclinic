from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Examen
from .forms import ExamenForm
@login_required
def lista(request):
    qs=Examen.objects.select_related('paciente','tipo','veterinario').order_by('-fecha_solicitud')
    return render(request,'examenes/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def detalle(request,pk): return render(request,'examenes/detalle.html',{'obj':get_object_or_404(Examen,pk=pk)})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=ExamenForm(request.POST or None,request.FILES or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Examen registrado.');return redirect('examenes:detalle',pk=obj.pk)
    return render(request,'examenes/form.html',{'form':form,'titulo':'Nuevo examen'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Examen,pk=pk)
    form=ExamenForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('examenes:detalle',pk=obj.pk)
    return render(request,'examenes/form.html',{'form':form,'titulo':'Editar examen','obj':obj})
