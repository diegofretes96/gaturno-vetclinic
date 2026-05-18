from django import forms
from .models import Internamiento,EvolucionDiaria
class InternamientoForm(forms.ModelForm):
    class Meta:
        model=Internamiento
        fields=['paciente','habitacion','veterinario','motivo_ingreso','diagnostico_ingreso','dieta','estado','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'habitacion':forms.Select(attrs={'class':'form-select'}),'veterinario':forms.Select(attrs={'class':'form-select'}),'motivo_ingreso':forms.Textarea(attrs={'class':'form-control','rows':2}),'diagnostico_ingreso':forms.Textarea(attrs={'class':'form-control','rows':2}),'dieta':forms.Textarea(attrs={'class':'form-control','rows':2}),'estado':forms.Select(attrs={'class':'form-select'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
class EvolucionForm(forms.ModelForm):
    class Meta:
        model=EvolucionDiaria
        fields=['veterinario','peso','temperatura','fc','fr','estado_general','alimentacion','descripcion','plan']
        widgets={'veterinario':forms.Select(attrs={'class':'form-select'}),'peso':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'temperatura':forms.NumberInput(attrs={'class':'form-control','step':'0.1'}),'fc':forms.NumberInput(attrs={'class':'form-control'}),'fr':forms.NumberInput(attrs={'class':'form-control'}),'estado_general':forms.TextInput(attrs={'class':'form-control'}),'alimentacion':forms.TextInput(attrs={'class':'form-control'}),'descripcion':forms.Textarea(attrs={'class':'form-control','rows':4}),'plan':forms.Textarea(attrs={'class':'form-control','rows':3})}
