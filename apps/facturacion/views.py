from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils import timezone
from .models import Factura, ItemFactura
from .forms import FacturaForm, ItemFacturaForm


@login_required
def lista(request):
    qs = Factura.objects.select_related('propietario', 'paciente').order_by('-fecha_emision')
    estado = request.GET.get('estado', '')
    if estado:
        qs = qs.filter(estado=estado)
    hoy = timezone.now().date()
    stats = {
        'hoy': Factura.objects.filter(fecha_emision__date=hoy, estado='pagada').aggregate(t=Sum('total'))['t'] or 0,
        'mes': Factura.objects.filter(fecha_emision__month=hoy.month, fecha_emision__year=hoy.year, estado='pagada').aggregate(t=Sum('total'))['t'] or 0,
        'pendientes': Factura.objects.filter(estado__in=['borrador', 'emitida']).count(),
    }
    return render(request, 'facturacion/lista.html', {
        'facturas': Paginator(qs, 25).get_page(request.GET.get('page')),
        'stats': stats,
        'estado_sel': estado,
        'estados': Factura.ESTADOS,
    })


@login_required
def detalle(request, pk):
    obj = get_object_or_404(
        Factura.objects.prefetch_related('items__producto').select_related('propietario', 'paciente', 'creado_por'),
        pk=pk,
    )
    return render(request, 'facturacion/detalle.html', {'factura': obj, 'form_item': ItemFacturaForm()})


@login_required
def crear(request):
    initial = {}
    if request.GET.get('propietario'):
        initial['propietario'] = request.GET['propietario']
    form = FacturaForm(request.POST or None, initial=initial)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.creado_por = request.user
        obj.save()
        messages.success(request, 'Factura creada.')
        return redirect('facturacion:detalle', pk=obj.pk)
    return render(request, 'facturacion/form.html', {'form': form, 'titulo': 'Nueva factura'})


@login_required
def editar(request, pk):
    obj = get_object_or_404(Factura, pk=pk)
    form = FacturaForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Actualizado.')
        return redirect('facturacion:detalle', pk=obj.pk)
    return render(request, 'facturacion/form.html', {'form': form, 'titulo': 'Editar factura', 'obj': obj})


@login_required
def agregar_item(request, pk):
    f = get_object_or_404(Factura, pk=pk)
    form = ItemFacturaForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.factura = f
        item.save()
        f.calcular_totales()
        messages.success(request, 'Ítem agregado.')
    return redirect('facturacion:detalle', pk=pk)


@login_required
def eliminar_item(request, pk, item_pk):
    item = get_object_or_404(ItemFactura, pk=item_pk, factura__pk=pk)
    f = item.factura
    item.delete()
    f.calcular_totales()
    messages.success(request, 'Ítem eliminado.')
    return redirect('facturacion:detalle', pk=pk)


@login_required
def cobrar(request, pk):
    f = get_object_or_404(Factura, pk=pk)
    if request.method == 'POST':
        # Verificar stock antes de confirmar el pago
        items_con_producto = f.items.filter(producto__isnull=False).select_related('producto')
        sin_stock = []
        for item in items_con_producto:
            if item.producto.stock_actual < item.cantidad:
                sin_stock.append(
                    f"{item.producto.nombre}: necesita {item.cantidad}, disponible {item.producto.stock_actual}"
                )

        if sin_stock:
            for msg in sin_stock:
                messages.error(request, f"Stock insuficiente — {msg}")
            return redirect('facturacion:detalle', pk=pk)

        # Registrar pago
        f.metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        f.monto_pagado = f.total
        f.estado = 'pagada'
        f.save()

        # Descontar stock y registrar movimientos
        _descontar_stock_factura(items_con_producto, request.user, f.numero)

        messages.success(request, 'Pago registrado y stock actualizado.')
        return redirect('facturacion:detalle', pk=pk)

    return render(request, 'facturacion/cobrar.html', {'factura': f, 'metodos': Factura.METODOS})


@login_required
def imprimir(request, pk):
    return render(request, 'facturacion/imprimir.html', {
        'factura': get_object_or_404(
            Factura.objects.prefetch_related('items').select_related('propietario', 'paciente'),
            pk=pk,
        )
    })


# ── helper ──────────────────────────────────────────────────────────────────

def _descontar_stock_factura(items_con_producto, usuario, numero_factura):
    """Genera un MovimientoStock tipo 'salida' por cada ítem de producto al cobrar."""
    from apps.inventario.models import MovimientoStock
    for item in items_con_producto:
        p = item.producto
        stock_anterior = p.stock_actual
        p.stock_actual -= item.cantidad
        p.save(update_fields=['stock_actual'])
        MovimientoStock.objects.create(
            producto=p,
            tipo='salida',
            cantidad=item.cantidad,
            stock_anterior=stock_anterior,
            stock_resultante=p.stock_actual,
            motivo=f'Venta – Factura {numero_factura}',
            usuario=usuario,
        )
