from django import forms
from .models import Vacunacion,Vacuna
class VacunacionForm(forms.ModelForm):
    class Meta:
        model=Vacunacion
        fields=['paciente','vacuna','veterinario','fecha_aplicacion','lote','dosis','via','sitio','proxima_dosis','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'vacuna':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'fecha_aplicacion':forms.DateInput(attrs={'class':'form-control','type':'date'}),'lote':forms.TextInput(attrs={'class':'form-control'}),'dosis':forms.TextInput(attrs={'class':'form-control'}),'via':forms.TextInput(attrs={'class':'form-control'}),'sitio':forms.TextInput(attrs={'class':'form-control'}),'proxima_dosis':forms.DateInput(attrs={'class':'form-control','type':'date'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
class VacunaForm(forms.ModelForm):
    class Meta:
        model=Vacuna
        fields=['nombre','fabricante','especie','intervalo_dias','descripcion','activo']
        widgets={'nombre':forms.TextInput(attrs={'class':'form-control'}),'fabricante':forms.TextInput(attrs={'class':'form-control'}),'especie':forms.Select(attrs={'class':'form-select'}),'intervalo_dias':forms.NumberInput(attrs={'class':'form-control'}),'descripcion':forms.Textarea(attrs={'class':'form-control','rows':2}),'activo':forms.CheckboxInput(attrs={'class':'form-check-input'})}
