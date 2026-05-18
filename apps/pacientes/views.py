from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Paciente,Especie,Raza
from .forms import PacienteForm

@login_required
def lista(request):
    q=request.GET.get('q',''); esp=request.GET.get('especie','')
    qs=Paciente.objects.select_related('propietario','especie','raza')
    if q: qs=qs.filter(Q(nombre__icontains=q)|Q(propietario__apellidos__icontains=q)|Q(propietario__nombres__icontains=q)|Q(microchip__icontains=q))
    if esp: qs=qs.filter(especie__id=esp)
    return render(request,'pacientes/lista.html',{'pacientes':Paginator(qs.order_by('nombre'),25).get_page(request.GET.get('page')),'especies':Especie.objects.all(),'q':q,'especie_sel':esp})

@login_required
def detalle(request,pk):
    pac=get_object_or_404(Paciente.objects.select_related('propietario','especie','raza'),pk=pk)
    return render(request,'pacientes/detalle.html',{
        'paciente':pac,
        'consultas':pac.consultas.select_related('veterinario').order_by('-fecha')[:10],
        'vacunaciones':pac.vacunaciones.select_related('vacuna','veterinario').order_by('-fecha_aplicacion')[:10],
        'desparasitaciones':pac.desparasitaciones.order_by('-fecha_aplicacion')[:10],
        'examenes':pac.examenes.select_related('tipo').order_by('-fecha_solicitud')[:10],
        'cirugias':pac.cirugias.select_related('cirujano').order_by('-fecha_programada')[:10],
        'internamientos':pac.internamientos.select_related('habitacion','veterinario').order_by('-fecha_ingreso')[:5],
        'citas':pac.citas.filter(estado__in=['pendiente','confirmada']).order_by('fecha')[:5],
        'estetica':pac.servicios_estetica.order_by('-fecha')[:5],
        'certificados':pac.certificados.order_by('-fecha_emision')[:5],
    })

@login_required
def crear(request):
    initial={}
    if request.GET.get('propietario'): initial['propietario']=request.GET['propietario']
    form=PacienteForm(request.POST or None,request.FILES or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,f'Paciente {obj.nombre} registrado.');return redirect('pacientes:detalle',pk=obj.pk)
    return render(request,'pacientes/form.html',{'form':form,'titulo':'Nuevo paciente'})

@login_required
def editar(request,pk):
    obj=get_object_or_404(Paciente,pk=pk)
    form=PacienteForm(request.POST or None,request.FILES or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('pacientes:detalle',pk=obj.pk)
    return render(request,'pacientes/form.html',{'form':form,'titulo':'Editar paciente','obj':obj})

@login_required
def eliminar(request,pk):
    obj=get_object_or_404(Paciente,pk=pk)
    if request.method=='POST':
        obj.estado='dado_baja';obj.save();messages.success(request,'Paciente dado de baja.');return redirect('pacientes:lista')
    return render(request,'pacientes/confirmar.html',{'obj':obj,'titulo':obj.nombre})

def razas_ajax(request):
    razas=list(Raza.objects.filter(especie_id=request.GET.get('especie_id',0)).values('id','nombre'))
    return JsonResponse({'razas':razas})

def buscar_ajax(request):
    q=request.GET.get('q','')
    qs=Paciente.objects.filter(Q(nombre__icontains=q)|Q(propietario__apellidos__icontains=q)).select_related('especie','propietario')[:8]
    return JsonResponse({'results':[{'nombre':p.nombre,'especie':p.especie.nombre,'propietario':p.propietario.nombre_completo,'url':f'/pacientes/{p.pk}/'} for p in qs]})
