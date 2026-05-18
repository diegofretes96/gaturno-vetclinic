from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Desparasitacion
from .forms import DesparasitacionForm
@login_required
def lista(request):
    qs=Desparasitacion.objects.select_related('paciente','veterinario').order_by('-fecha_aplicacion')
    return render(request,'desparasitacion/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=DesparasitacionForm(request.POST or None,initial=initial)
    if form.is_valid():
        form.save();messages.success(request,'Desparasitación registrada.');return redirect('desparasitacion:lista')
    return render(request,'desparasitacion/form.html',{'form':form,'titulo':'Nueva desparasitación'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Desparasitacion,pk=pk)
    form=DesparasitacionForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('desparasitacion:lista')
    return render(request,'desparasitacion/form.html',{'form':form,'titulo':'Editar','obj':obj})
