from django import forms
from .models import Medicamento
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model=Medicamento
        fields=['nombre_comercial','nombre_generico','principio_activo','concentracion','forma_farmaceutica','laboratorio','indicaciones','contraindicaciones','dosis_recomendada','via_administracion','especies','requiere_receta','activo']
        widgets={f:forms.TextInput(attrs={'class':'form-control'}) for f in ['nombre_comercial','nombre_generico','principio_activo','concentracion','forma_farmaceutica','laboratorio','via_administracion']}
        widgets['indicaciones']=forms.Textarea(attrs={'class':'form-control','rows':3})
        widgets['contraindicaciones']=forms.Textarea(attrs={'class':'form-control','rows':3})
        widgets['dosis_recomendada']=forms.Textarea(attrs={'class':'form-control','rows':3})
        widgets['especies']=forms.CheckboxSelectMultiple()
        widgets['requiere_receta']=forms.CheckboxInput(attrs={'class':'form-check-input'})
        widgets['activo']=forms.CheckboxInput(attrs={'class':'form-check-input'})
