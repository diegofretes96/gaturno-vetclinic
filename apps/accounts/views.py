from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from .models import Usuario
from .forms import LoginForm, UsuarioForm, UsuarioEditForm

def login_view(request):
    if request.user.is_authenticated: return redirect('reportes:dashboard')
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next', '/'))
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request); return redirect('accounts:login')

@login_required
def lista(request):
    return render(request, 'accounts/lista.html', {'usuarios': Usuario.objects.all().order_by('last_name','first_name')})

@login_required
def crear(request):
    form = UsuarioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(); messages.success(request,'Usuario creado.'); return redirect('accounts:lista')
    return render(request, 'accounts/form.html', {'form': form,'titulo': 'Nuevo usuario'})

@login_required
def editar(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    form = UsuarioEditForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request,'Usuario actualizado.'); return redirect('accounts:lista')
    return render(request, 'accounts/form.html', {'form': form,'titulo': 'Editar usuario','obj': obj})

@login_required
def perfil(request):
    return render(request, 'accounts/perfil.html', {'usuario': request.user})


@login_required
def cambiar_password(request, pk):
    # Solo admins pueden cambiar la contraseña de otros usuarios
    # Cualquier usuario puede cambiar la propia
    obj = get_object_or_404(Usuario, pk=pk)
    if obj != request.user and not request.user.is_superuser and request.user.rol != 'admin':
        messages.error(request, 'No tenés permisos para cambiar la contraseña de otro usuario.')
        return redirect('accounts:lista')

    form = SetPasswordForm(user=obj, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        # Si el usuario cambia su propia contraseña, mantener la sesión activa
        if obj == request.user:
            update_session_auth_hash(request, obj)
        messages.success(request, f'Contraseña de {obj.username} actualizada correctamente.')
        return redirect('accounts:lista')

    return render(request, 'accounts/cambiar_password.html', {
        'form': form,
        'obj': obj,
        'titulo': f'Cambiar contraseña — {obj.username}',
    })
