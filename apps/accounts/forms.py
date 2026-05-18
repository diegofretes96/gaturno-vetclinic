from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','first_name','last_name','email','rol','telefono','matricula','especialidad']
        widgets = {f: forms.TextInput(attrs={'class':'form-control'}) for f in ['username','first_name','last_name','email','telefono','matricula','especialidad']}
        widgets['rol'] = forms.Select(attrs={'class':'form-select'})

class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name','last_name','email','rol','telefono','matricula','especialidad','foto']
        widgets = {f: forms.TextInput(attrs={'class':'form-control'}) for f in ['first_name','last_name','email','telefono','matricula','especialidad']}
        widgets['rol'] = forms.Select(attrs={'class':'form-select'})
        widgets['foto'] = forms.FileInput(attrs={'class':'form-control'})
