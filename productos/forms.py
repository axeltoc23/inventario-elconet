from django import forms
from .models import MovimientoInventario, Producto, Ubicacion


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre']


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["tipo", "cantidad", "comentario"]


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'ubicacion', 'alerta_stock', 'alerta_activa', 'activo']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        producto_id = self.instance.id
        # Verificamos si ya existe un producto con el mismo nombre, no importando que tenga mayusculas o minusculas
        if Producto.objects.filter(nombre__iexact=nombre).exclude(id=producto_id).exists():
            raise forms.ValidationError("Ya existe un producto con ese nombre. Por favor, elige otro.")
        return nombre
