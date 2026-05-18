from django import forms
from .models import Consulta,NotaClinica,Prescripcion
class ConsultaForm(forms.ModelForm):
    class Meta:
        model=Consulta
        fields=['paciente','veterinario','tipo','motivo_consulta','anamnesis','peso','temperatura','fc','fr','mucosas','linfonodos','condicion_corporal','subjetivo','objetivo','evaluacion','plan','diagnostico_presuntivo','diagnostico_definitivo','pronostico','observaciones','proxima_cita']
        widgets={
            'paciente':forms.Select(attrs={'class':'form-select'}),
            'veterinario':forms.Select(attrs={'class':'form-select'}),
            'tipo':forms.Select(attrs={'class':'form-select'}),
            'motivo_consulta':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'anamnesis':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'peso':forms.NumberInput(attrs={'class':'form-control','step':'0.01','placeholder':'kg'}),
            'temperatura':forms.NumberInput(attrs={'class':'form-control','step':'0.1','placeholder':'°C'}),
            'fc':forms.NumberInput(attrs={'class':'form-control','placeholder':'lpm'}),
            'fr':forms.NumberInput(attrs={'class':'form-control','placeholder':'rpm'}),
            'mucosas':forms.TextInput(attrs={'class':'form-control'}),
            'linfonodos':forms.TextInput(attrs={'class':'form-control'}),
            'condicion_corporal':forms.NumberInput(attrs={'class':'form-control','min':1,'max':9}),
            'subjetivo':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'objetivo':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'evaluacion':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'plan':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'diagnostico_presuntivo':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'diagnostico_definitivo':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'pronostico':forms.TextInput(attrs={'class':'form-control'}),
            'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'proxima_cita':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }
class PrescripcionForm(forms.ModelForm):
    class Meta:
        model=Prescripcion
        fields=['medicamento_nombre','dosis','frecuencia','duracion','via','indicaciones']
        widgets={f:forms.TextInput(attrs={'class':'form-control'}) for f in ['medicamento_nombre','dosis','frecuencia','duracion','via']}
        widgets['indicaciones']=forms.Textarea(attrs={'class':'form-control','rows':2})
class NotaClinicaForm(forms.ModelForm):
    class Meta:
        model=NotaClinica
        fields=['nota']
        widgets={'nota':forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Agregar nota clínica…'})}
