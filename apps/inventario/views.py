from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto,MovimientoStock,Proveedor
from .forms import ProductoForm,MovimientoForm,ProveedorForm
@login_required
def lista(request):
    q=request.GET.get('q','');tipo=request.GET.get('tipo','')
    qs=Producto.objects.filter(activo=True).select_related('categoria','proveedor')
    if q: qs=qs.filter(Q(nombre__icontains=q)|Q(codigo__icontains=q))
    if tipo: qs=qs.filter(tipo=tipo)
    bajo_stock=[p for p in Producto.objects.filter(activo=True) if p.bajo_stock]
    return render(request,'inventario/lista.html',{'productos':Paginator(qs,25).get_page(request.GET.get('page')),'bajo_stock':bajo_stock,'q':q,'tipo_sel':tipo,'tipos':Producto.TIPOS})
@login_required
def detalle(request,pk):
    obj=get_object_or_404(Producto,pk=pk)
    return render(request,'inventario/detalle.html',{'obj':obj,'movimientos':obj.movimientos.select_related('usuario').order_by('-fecha')[:20]})
@login_required
def crear(request):
    form=ProductoForm(request.POST or None)
    if form.is_valid():
        obj=form.save();messages.success(request,'Producto creado.');return redirect('inventario:detalle',pk=obj.pk)
    return render(request,'inventario/form.html',{'form':form,'titulo':'Nuevo producto'})
@login_required
def editar(request,pk):
    obj=get_object_or_404(Producto,pk=pk)
    form=ProductoForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save();messages.success(request,'Actualizado.');return redirect('inventario:detalle',pk=obj.pk)
    return render(request,'inventario/form.html',{'form':form,'titulo':'Editar producto','obj':obj})
@login_required
def movimiento(request):
    form=MovimientoForm(request.POST or None)
    if form.is_valid():
        mov=form.save(commit=False);p=mov.producto;mov.stock_anterior=p.stock_actual
        if mov.tipo=='entrada': p.stock_actual+=mov.cantidad
        elif mov.tipo in ['salida','vencimiento']: p.stock_actual-=mov.cantidad
        else: p.stock_actual=mov.cantidad
        mov.stock_resultante=p.stock_actual;mov.usuario=request.user;mov.save();p.save()
        messages.success(request,'Movimiento registrado.');return redirect('inventario:lista')
    return render(request,'inventario/form_movimiento.html',{'form':form,'titulo':'Registrar movimiento'})
@login_required
def proveedores(request): return render(request,'inventario/proveedores.html',{'proveedores':Proveedor.objects.all()})
@login_required
def crear_proveedor(request):
    form=ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save();messages.success(request,'Proveedor creado.');return redirect('inventario:proveedores')
    return render(request,'inventario/form.html',{'form':form,'titulo':'Nuevo proveedor'})
