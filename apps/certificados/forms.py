from django import forms
from .models import Certificado
class CertificadoForm(forms.ModelForm):
    class Meta:
        model=Certificado
        fields=['paciente','veterinario','tipo','fecha_vencimiento','contenido','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'tipo':forms.Select(attrs={'class':'form-select'}),'fecha_vencimiento':forms.DateInput(attrs={'class':'form-control','type':'date'}),'contenido':forms.Textarea(attrs={'class':'form-control','rows':10}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
