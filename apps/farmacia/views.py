from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Receta,ItemReceta
from .forms import RecetaForm,ItemRecetaForm
@login_required
def lista(request):
    qs=Receta.objects.select_related('paciente','veterinario').order_by('-fecha_emision')
    return render(request,'farmacia/lista.html',{'items':Paginator(qs,25).get_page(request.GET.get('page'))})
@login_required
def detalle(request,pk):
    obj=get_object_or_404(Receta.objects.select_related('paciente','veterinario').prefetch_related('items__producto'),pk=pk)
    return render(request,'farmacia/detalle.html',{'obj':obj,'form':ItemRecetaForm()})
@login_required
def crear(request):
    initial={}
    if request.GET.get('paciente'): initial['paciente']=request.GET['paciente']
    if request.user.es_veterinario: initial['veterinario']=request.user.pk
    form=RecetaForm(request.POST or None,initial=initial)
    if form.is_valid():
        obj=form.save();messages.success(request,'Receta creada.');return redirect('farmacia:detalle',pk=obj.pk)
    return render(request,'farmacia/form.html',{'form':form,'titulo':'Nueva receta'})
@login_required
def agregar_item(request,pk):
    receta=get_object_or_404(Receta,pk=pk)
    form=ItemRecetaForm(request.POST)
    if form.is_valid():
        item=form.save(commit=False);item.receta=receta;item.save()
        messages.success(request,'Ítem agregado.')
    return redirect('farmacia:detalle',pk=pk)
@login_required
def despachar(request,pk):
    receta=get_object_or_404(Receta,pk=pk)
    if request.method=='POST':
        from apps.inventario.models import MovimientoStock
        for item in receta.items.filter(despachado=False):
            p=item.producto;ant=p.stock_actual;p.stock_actual-=item.cantidad_despachar
            MovimientoStock.objects.create(producto=p,tipo='salida',cantidad=item.cantidad_despachar,stock_anterior=ant,stock_resultante=p.stock_actual,motivo=f'Receta #{receta.pk}',usuario=request.user)
            p.save();item.despachado=True;item.save()
        receta.estado='despachada';receta.save()
        messages.success(request,'Receta despachada.');return redirect('farmacia:lista')
    return render(request,'farmacia/confirmar_despacho.html',{'receta':receta})
