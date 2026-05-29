import urllib.parse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ConfigSite, GaleriaFoto, ProductoWeb
from .forms import ContactoForm


def landing(request):
    config = ConfigSite.get()
    fotos = GaleriaFoto.objects.filter(activo=True)
    productos = ProductoWeb.objects.filter(disponible=True)
    form = ContactoForm()
    return render(request, 'landing/index.html', {
        'config': config,
        'fotos': fotos,
        'productos': productos,
        'form': form,
    })


def contacto(request):
    if request.method != 'POST':
        return redirect('landing:landing')

    config = ConfigSite.get()
    form = ContactoForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Por favor completá los campos requeridos.')
        return redirect('landing:landing')

    nombre = form.cleaned_data['nombre']
    email = form.cleaned_data.get('email', '')
    telefono = form.cleaned_data.get('telefono', '')
    mensaje = form.cleaned_data['mensaje']
    canal = request.POST.get('canal', 'email')

    if canal == 'whatsapp' and config.whatsapp:
        texto = f"Hola Gaturno! Soy {nombre}"
        if telefono:
            texto += f" (tel: {telefono})"
        texto += f". {mensaje}"
        wa_url = f"https://wa.me/{config.whatsapp}?text={urllib.parse.quote(texto)}"
        return redirect(wa_url)

    # Canal email
    if config.email_contacto:
        cuerpo = f"Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\n\nMensaje:\n{mensaje}"
        try:
            send_mail(
                subject=f'[Gaturno Web] Consulta de {nombre}',
                message=cuerpo,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@gaturno.com'),
                recipient_list=[config.email_contacto],
                fail_silently=True,
            )
        except Exception:
            pass

    messages.success(request, f'¡Gracias {nombre}! Recibimos tu mensaje y te contactaremos pronto.')
    return redirect('landing:landing')
