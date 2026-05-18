from django import forms
from .models import Factura,ItemFactura
class FacturaForm(forms.ModelForm):
    class Meta:
        model=Factura
        fields=['propietario','paciente','fecha_emision','estado','metodo_pago','descuento','observaciones']
        widgets={'propietario':forms.Select(attrs={'class':'form-select'}),'paciente':forms.Select(attrs={'class':'form-select'}),'fecha_emision':forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}),'estado':forms.Select(attrs={'class':'form-select'}),'metodo_pago':forms.Select(attrs={'class':'form-select'}),'descuento':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'observaciones':forms.Textarea(attrs={'class':'form-control','rows':2})}
class ItemFacturaForm(forms.ModelForm):
    class Meta:
        model=ItemFactura
        fields=['descripcion','producto','cantidad','precio_unitario','descuento_item']
        widgets={'descripcion':forms.TextInput(attrs={'class':'form-control'}),'producto':forms.Select(attrs={'class':'form-select'}),'cantidad':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'precio_unitario':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'descuento_item':forms.NumberInput(attrs={'class':'form-control','step':'0.01'})}
