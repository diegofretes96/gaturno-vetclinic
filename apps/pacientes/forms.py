from django import forms
from .models import Paciente,Raza
class PacienteForm(forms.ModelForm):
    class Meta:
        model=Paciente
        fields=['propietario','nombre','especie','raza','sexo','fecha_nacimiento','color','peso','microchip','esterilizado','foto','alergias','antecedentes','estado']
        widgets={
            'propietario':forms.Select(attrs={'class':'form-select'}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'especie':forms.Select(attrs={'class':'form-select','id':'id_especie'}),
            'raza':forms.Select(attrs={'class':'form-select','id':'id_raza'}),
            'sexo':forms.Select(attrs={'class':'form-select'}),
            'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'color':forms.TextInput(attrs={'class':'form-control'}),
            'peso':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
            'microchip':forms.TextInput(attrs={'class':'form-control'}),
            'esterilizado':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'foto':forms.FileInput(attrs={'class':'form-control','accept':'image/*'}),
            'alergias':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'antecedentes':forms.Textarea(attrs={'class':'form-control','rows':2}),
            'estado':forms.Select(attrs={'class':'form-select'}),
        }
