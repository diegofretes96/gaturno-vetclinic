from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Medicamento
from .forms import MedicamentoForm
@login_required
def lista(request):
    q=request.GET.get('q','')
    qs=Medicamento.objects.filter(activo=True)
    if q: qs=qs.filter(Q(nombre_comercial__icontains=q)|Q(nombre_generico__icontains=q)|Q(principio_activo__icontains=q))
    return render(request,'vademecum/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page')),'q':q})
@login_required
def detalle(request,pk): return render(request,'vademecum/detalle.html',{'obj':get_object_or_404(Medicamento,pk=pk)})
@login_required
def crear(request):
    form=MedicamentoForm(request.POST or None)
    if form.is_valid():
        obj=form.save();messages.success(request,'Medicamento registrado.');return redirect('vademecum:detalle',pk=obj.pk)
    return render(request,'vademecum/form.html',{'form':form,'titulo':'Nuevo medicamento'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Medicamento,pk=pk)
    form=MedicamentoForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('vademecum:detalle',pk=obj.pk)
    return render(request,'vademecum/form.html',{'form':form,'titulo':'Editar medicamento','obj':obj})
