from django import forms
from .models import Cirugia
class CirugiaForm(forms.ModelForm):
    class Meta:
        model=Cirugia
        fields=['paciente','cirujano','anestesista','fecha_programada','procedimiento','descripcion','tipo_anestesia','protocolo_anestesico','hallazgos','complicaciones','estado','cuidados_post','observaciones']
        widgets={'paciente':forms.Select(attrs={'class':'form-select'}),'cirujano':forms.Select(attrs={'class':'form-select'}),'anestesista':forms.Select(attrs={'class':'form-select'}),'fecha_programada':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),'procedimiento':forms.TextInput(attrs={'class':'form-control'}),'descripcion':forms.Textarea(attrs={'class':'form-control','rows':3}),'tipo_anestesia':forms.Select(attrs={'class':'form-select'}),'protocolo_anestesico':forms.Textarea(attrs={'class':'form-control','rows':2}),'hallazgos':forms.Textarea(attrs={'class':'form-control','rows':3}),'complicaciones':forms.Textarea(attrs={'class':'form-control','rows':2}),'estado':forms.Select(attrs={'class':'form-select'}),'cuidados_post':forms.Textarea(attrs={'class':'form-control','rows':3}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
