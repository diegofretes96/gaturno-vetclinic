from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Propietario, DatosFacturacion
from .forms import PropietarioForm, DatosFacturacionForm


@login_required
def lista(request):
    q = request.GET.get('q', '')
    qs = Propietario.objects.all()
    if q:
        qs = qs.filter(
            Q(nombres__icontains=q) | Q(apellidos__icontains=q) |
            Q(numero_documento__icontains=q) | Q(telefono__icontains=q)
        )
    return render(request, 'propietarios/lista.html', {
        'propietarios': Paginator(qs.order_by('apellidos', 'nombres'), 25).get_page(request.GET.get('page')),
        'q': q,
    })


@login_required
def detalle(request, pk):
    obj = get_object_or_404(Propietario, pk=pk)
    return render(request, 'propietarios/detalle.html', {
        'propietario': obj,
        'mascotas': obj.mascotas.all(),
    })


@login_required
def crear(request):
    form = PropietarioForm(request.POST or None)
    factura_form = DatosFacturacionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        _guardar_datos_facturacion(request.POST, obj)
        messages.success(request, 'Propietario registrado.')
        return redirect('propietarios:detalle', pk=obj.pk)
    return render(request, 'propietarios/form.html', {
        'form': form,
        'factura_form': factura_form,
        'titulo': 'Nuevo propietario',
    })


@login_required
def editar(request, pk):
    obj = get_object_or_404(Propietario, pk=pk)
    datos_fc = getattr(obj, 'datos_facturacion', None)
    form = PropietarioForm(request.POST or None, instance=obj)
    factura_form = DatosFacturacionForm(request.POST or None, instance=datos_fc)
    if request.method == 'POST' and form.is_valid():
        form.save()
        _guardar_datos_facturacion(request.POST, obj)
        messages.success(request, 'Actualizado.')
        return redirect('propietarios:detalle', pk=obj.pk)
    return render(request, 'propietarios/form.html', {
        'form': form,
        'factura_form': factura_form,
        'titulo': 'Editar propietario',
        'obj': obj,
    })


@login_required
def eliminar(request, pk):
    obj = get_object_or_404(Propietario, pk=pk)
    if request.method == 'POST':
        obj.activo = False
        obj.save()
        messages.success(request, 'Desactivado.')
        return redirect('propietarios:lista')
    return render(request, 'propietarios/confirmar.html', {'obj': obj, 'titulo': obj.nombre_completo})


# ── helper ──────────────────────────────────────────────────────────────────

def _guardar_datos_facturacion(post_data, propietario):
    razon_social = post_data.get('razon_social', '').strip()
    ruc = post_data.get('ruc', '').strip()
    if razon_social:
        DatosFacturacion.objects.update_or_create(
            propietario=propietario,
            defaults={'razon_social': razon_social, 'ruc': ruc},
        )
    else:
        # Si vaciaron los campos, eliminar los datos de facturación existentes
        DatosFacturacion.objects.filter(propietario=propietario).delete()
