from django import forms
from .models import Desparasitacion
class DesparasitacionForm(forms.ModelForm):
    class Meta:
        model=Desparasitacion
        fields=['paciente','veterinario','tipo','producto_nombre','dosis','fecha_aplicacion','proxima_aplicacion','peso_momento','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'tipo':forms.Select(attrs={'class':'form-select'}),'producto_nombre':forms.TextInput(attrs={'class':'form-control'}),'dosis':forms.TextInput(attrs={'class':'form-control'}),'fecha_aplicacion':forms.DateInput(attrs={'class':'form-control','type':'date'}),'proxima_aplicacion':forms.DateInput(attrs={'class':'form-control','type':'date'}),'peso_momento':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
