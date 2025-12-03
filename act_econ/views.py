from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  *
from .models import  *
from .forms import *


@login_required
def listar_empresas_contribuyente(request):
    # Obtener el contribuyente asociado al usuario logueado
    
    contribuyentes = Contribuyente.objects.get(users=request.user)
    
    usuario = request.user
    
    # Obtener todas las empresas del contribuyente
    empresas = Empresas.objects.filter(contribuyentes=contribuyentes)
    
    # Procesar el formulario si se envió
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.contribuyente = contribuyentes
            empresa.save()
            messages.success(request, f'Empresa "{Empresas.razon_social}" registrada exitosamente.')
            return redirect('listar_empresas_contribuyente')
    else:
        form = EmpresaForm()
    
    context = {
        'contribuyente': contribuyentes,
        'empresas': empresas,
        'form': form,
    }

    
    return render(request, 'actecon/listar_empresas.html', context)