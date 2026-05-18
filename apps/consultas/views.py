from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Consulta,NotaClinica,Prescripcion
from .forms import ConsultaForm,PrescripcionForm,NotaClinicaForm
from apps.agenda.models import Cita

@login_required
def lista(request):
    qs=Consulta.objects.select_related('paciente','veterinario').order_by('-fecha')
    return render(request,'consultas/lista.html',{'consultas':Paginator(qs,25).get_page(request.GET.get('page'))})

@login_required
def detalle(request,pk):
    obj=get_object_or_404(Consulta.objects.select_related('paciente','veterinario').prefetch_related('notas__veterinario','prescripciones'),pk=pk)
    return render(request,'consultas/detalle.html',{'consulta':obj,'form_nota':NotaClinicaForm(),'form_rx':PrescripcionForm()})

@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=ConsultaForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Consulta registrada.');return redirect('consultas:detalle',pk=obj.pk)
    return render(request,'consultas/form.html',{'form':form,'titulo':'Nueva consulta'})

@login_required
def nueva_desde_cita(request,pk):
    cita=get_object_or_404(Cita,pk=pk)
    initial={'paciente':cita.paciente.pk,'motivo_consulta':cita.motivo}
    if cita.veterinario: initial['veterinario']=cita.veterinario.pk
    form=ConsultaForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save(commit=False);obj.cita=cita;obj.save()
        cita.estado='realizada';cita.save()
        messages.success(request,'Consulta registrada.');return redirect('consultas:detalle',pk=obj.pk)
    return render(request,'consultas/form.html',{'form':form,'titulo':'Nueva consulta','cita':cita})

@login_required
def editar(request,pk):
    obj=get_object_or_404(Consulta,pk=pk)
    form=ConsultaForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('consultas:detalle',pk=obj.pk)
    return render(request,'consultas/form.html',{'form':form,'titulo':'Editar consulta','obj':obj})

@login_required
def agregar_nota(request,pk):
    c=get_object_or_404(Consulta,pk=pk)
    form=NotaClinicaForm(request.POST)
    if form.is_valid():
        n=form.save(commit=False);n.consulta=c;n.veterinario=request.user;n.save()
        messages.success(request,'Nota agregada.')
    return redirect('consultas:detalle',pk=pk)

@login_required
def agregar_prescripcion(request,pk):
    c=get_object_or_404(Consulta,pk=pk)
    form=PrescripcionForm(request.POST)
    if form.is_valid():
        rx=form.save(commit=False);rx.consulta=c;rx.save()
        messages.success(request,'Prescripción agregada.')
    return redirect('consultas:detalle',pk=pk)

@login_required
def imprimir(request,pk):
    obj=get_object_or_404(Consulta.objects.select_related('paciente__propietario','veterinario').prefetch_related('prescripciones'),pk=pk)
    return render(request,'consultas/imprimir.html',{'consulta':obj})
