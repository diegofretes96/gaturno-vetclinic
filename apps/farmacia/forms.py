from django import forms
from .models import Receta,ItemReceta
class RecetaForm(forms.ModelForm):
    class Meta:
        model=Receta
        fields=['paciente','veterinario','consulta','fecha_vencimiento','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'consulta':forms.Select(attrs={'class':'form-select'}),'fecha_vencimiento':forms.DateInput(attrs={'class':'form-control','type':'date'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
class ItemRecetaForm(forms.ModelForm):
    class Meta:
        model=ItemReceta
        fields=['producto','dosis','frecuencia','duracion','via','cantidad_despachar','indicaciones']
        widgets={'producto':forms.Select(attrs={'class':'form-select'}),'dosis':forms.TextInput(attrs={'class':'form-control'}),'frecuencia':forms.TextInput(attrs={'class':'form-control'}),'duracion':forms.TextInput(attrs={'class':'form-control'}),'via':forms.TextInput(attrs={'class':'form-control'}),'cantidad_despachar':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'indicaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
