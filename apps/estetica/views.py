from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Estetica
from .forms import EsteticaForm
@login_required
def lista(request):
    qs=Estetica.objects.select_related('paciente','esteticista').order_by('-fecha')
    return render(request,'estetica/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    form=EsteticaForm(request.POST or None,request.FILES or None,initial=initial)
    if form.is_valid():
        form.save();messages.success(request,'Servicio registrado.');return redirect('estetica:lista')
    return render(request,'estetica/form.html',{'form':form,'titulo':'Nuevo servicio estético'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Estetica,pk=pk)
    form=EsteticaForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('estetica:lista')
    return render(request,'estetica/form.html',{'form':form,'titulo':'Editar servicio','obj':obj})
@login_required
def completar(request,pk):
    obj=get_object_or_404(Estetica,pk=pk);obj.completado=True;obj.save()
    messages.success(request,'Servicio completado.');return redirect('estetica:lista')
