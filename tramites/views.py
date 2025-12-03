from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FormularioRegistroUsuario, FormularioPerfilContribuyente

def registro_contribuyente(request):
    if request.method == 'POST':
        form_usuario = FormularioRegistroUsuario(request.POST)
        form_perfil = FormularioPerfilContribuyente(request.POST)
        
        if form_usuario.is_valid() and form_perfil.is_valid():
            # Guardar usuario (NO es staff/admin)
            usuario = form_usuario.save()
            usuario.is_staff = False  # Asegurar que no sea administrador
            usuario.is_superuser = False
            usuario.save()
            
            # Guardar perfil del contribuyente
            perfil = form_perfil.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
            
            # Autenticar y loguear al usuario
            username = form_usuario.cleaned_data.get('username')
            password = form_usuario.cleaned_data.get('password1')
            usuario_auth = authenticate(username=username, password=password)
            login(request, usuario_auth)
            
            messages.success(request, '¡Registro exitoso! Bienvenido al sistema.')
            return redirect('dashboard_contribuyente')
    else:
        form_usuario = FormularioRegistroUsuario()
        form_perfil = FormularioPerfilContribuyente()
    
    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }
    return render(request, 'contribuyentes/registro.html', context)

@login_required
def dashboard_contribuyente(request):
    # Verificar que el usuario no sea admin
    if request.user.is_staff:
        messages.warning(request, 'Los administradores deben usar el panel de admin.')
        return redirect('admin:index')
    
    return render(request, 'contribuyentes/dashboard.html')


