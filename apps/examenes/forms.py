from django import forms
from .models import Examen
class ExamenForm(forms.ModelForm):
    class Meta:
        model=Examen
        fields=['paciente','tipo','veterinario','muestra','estado','resultado','interpretacion','archivo','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'tipo':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'muestra':forms.TextInput(attrs={'class':'form-control'}),'estado':forms.Select(attrs={'class':'form-select'}),'resultado':forms.Textarea(attrs={'class':'form-control','rows':4}),'interpretacion':forms.Textarea(attrs={'class':'form-control','rows':3}),'archivo':forms.FileInput(attrs={'class':'form-control'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
