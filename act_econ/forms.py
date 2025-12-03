from django import forms
from .models import Empresas

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['licencia', 'direccion', 'telefono', 'razon_social']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'licencia': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Licencia de empresa'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }