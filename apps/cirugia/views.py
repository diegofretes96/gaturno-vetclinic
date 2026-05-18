from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Cirugia
from .forms import CirugiaForm
@login_required
def lista(request):
    qs=Cirugia.objects.select_related('paciente','cirujano').order_by('-fecha_programada')
    return render(request,'cirugia/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def detalle(request,pk): return render(request,'cirugia/detalle.html',{'obj':get_object_or_404(Cirugia,pk=pk)})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['cirujano']=request.user.pk
    form=CirugiaForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Cirugía programada.');return redirect('cirugia:detalle',pk=obj.pk)
    return render(request,'cirugia/form.html',{'form':form,'titulo':'Nueva cirugía'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Cirugia,pk=pk)
    form=CirugiaForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('cirugia:detalle',pk=obj.pk)
    return render(request,'cirugia/form.html',{'form':form,'titulo':'Editar cirugía','obj':obj})
