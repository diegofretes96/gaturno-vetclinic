from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Certificado
from .forms import CertificadoForm
@login_required
def lista(request):
    qs=Certificado.objects.select_related('paciente','veterinario').order_by('-fecha_emision')
    return render(request,'certificados/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def detalle(request,pk): return render(request,'certificados/detalle.html',{'obj':get_object_or_404(Certificado,pk=pk)})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=CertificadoForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Certificado emitido.');return redirect('certificados:detalle',pk=obj.pk)
    return render(request,'certificados/form.html',{'form':form,'titulo':'Nuevo certificado'})
@login_required
def imprimir(request,pk): return render(request,'certificados/imprimir.html',{'obj':get_object_or_404(Certificado,pk=pk)})
