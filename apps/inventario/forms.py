from django import forms
from .models import Producto,Proveedor,MovimientoStock
class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['codigo','nombre','nombre_generico','tipo','categoria','proveedor','unidad_medida','precio_costo','precio_venta','stock_actual','stock_minimo','requiere_receta','descripcion','activo']
        widgets={'codigo':forms.TextInput(attrs={'class':'form-control'}),'nombre':forms.TextInput(attrs={'class':'form-control'}),'nombre_generico':forms.TextInput(attrs={'class':'form-control'}),'tipo':forms.Select(attrs={'class':'form-select'}),'categoria':forms.Select(attrs={'class':'form-select'}),'proveedor':forms.Select(attrs={'class':'form-select'}),'unidad_medida':forms.TextInput(attrs={'class':'form-control'}),'precio_costo':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'precio_venta':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'stock_actual':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'stock_minimo':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'requiere_receta':forms.CheckboxInput(attrs={'class':'form-check-input'}),'descripcion':forms.Textarea(attrs={'class':'form-control','rows':2}),'activo':forms.CheckboxInput(attrs={'class':'form-check-input'})}
class MovimientoForm(forms.ModelForm):
    class Meta:
        model=MovimientoStock
        fields=['producto','tipo','cantidad','motivo']
        widgets={'producto':forms.Select(attrs={'class':'form-select'}),'tipo':forms.Select(attrs={'class':'form-select'}),'cantidad':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),'motivo':forms.TextInput(attrs={'class':'form-control'})}
class ProveedorForm(forms.ModelForm):
    class Meta:
        model=Proveedor
        fields=['nombre','ruc','telefono','email','direccion','contacto','activo']
        widgets={f:forms.TextInput(attrs={'class':'form-control'}) for f in ['nombre','ruc','telefono','email','contacto']}
        widgets['direccion']=forms.Textarea(attrs={'class':'form-control','rows':2})
        widgets['activo']=forms.CheckboxInput(attrs={'class':'form-check-input'})
