from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tramites.models import *

class FormularioRegistroUsuario(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombres'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Apellidos'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class FormularioPerfilContribuyente(forms.ModelForm):
    class Meta:
        model = Contribuyente
        fields = ['ced_rif', 'tipo_contribuyente', 'direccion', 'telefono']
        widgets = {
            'ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese su ced-rif'
            }),
            'tipo_contribuyente': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            
        }
        labels = {
            'ced_rif': 'Rif/Cédula',
            'tipo_contribuyente': 'Tipo de Contribuyente',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            
        }