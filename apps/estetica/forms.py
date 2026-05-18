from django import forms
from .models import Estetica
class EsteticaForm(forms.ModelForm):
    class Meta:
        model=Estetica
        fields=['paciente','esteticista','servicio','fecha','duracion_horas','precio','observaciones','foto_antes','foto_despues']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'esteticista':forms.Select(attrs={'class':'form-select'}),'servicio':forms.Select(attrs={'class':'form-select'}),'fecha':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),'duracion_horas':forms.NumberInput(attrs={'class':'form-control'}),'precio':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2}),'foto_antes':forms.FileInput(attrs={'class':'form-control','accept':'image/*'}),'foto_despues':forms.FileInput(attrs={'class':'form-control','accept':'image/*'})}
