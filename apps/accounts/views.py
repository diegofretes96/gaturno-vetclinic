from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
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
