from django import forms
from .models import Cita,SalaEspera
class CitaForm(forms.ModelForm):
    class Meta:
        model=Cita
        fields=['paciente','veterinario','tipo','fecha','duracion_min','motivo','notas','estado']
        widgets={
            'paciente':forms.Select(attrs={'class':'form-select'}),
            'veterinario':forms.Select(attrs={'class':'form-select'}),
            'tipo':forms.Select(attrs={'class':'form-select'}),
            'fecha':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),
            'duracion_min':forms.NumberInput(attrs={'class':'form-control'}),
            'motivo':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'notas':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'estado':forms.Select(attrs={'class':'form-select'}),
        }
class SalaEsperaForm(forms.ModelForm):
    class Meta:
        model=SalaEspera
        fields=['cita','prioridad','notas_recepcion']
        widgets={'cita':forms.Select(attrs={'class':'form-select'}),'prioridad':forms.NumberInput(attrs={'class':'form-control'}),'notas_recepcion':forms.Textarea(attrs={'class':'form-control','rows':2})}
