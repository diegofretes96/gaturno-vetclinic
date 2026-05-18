from django import forms
from .models import Propietario, DatosFacturacion


class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = [
            'nombres', 'apellidos', 'tipo_documento', 'numero_documento',
            'telefono', 'telefono_alt', 'email',
            'direccion', 'ciudad', 'fecha_nacimiento', 'observaciones',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_alt': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_numero_documento(self):
        value = self.cleaned_data.get('numero_documento', '').strip()
        # Devolver None en lugar de cadena vacía para respetar unique=True con NULLs
        return value if value else None


class DatosFacturacionForm(forms.ModelForm):
    class Meta:
        model = DatosFacturacion
        fields = ['razon_social', 'ruc']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def has_data(self):
        return bool(self.data.get('razon_social', '').strip())
