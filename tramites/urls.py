from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'contribuyentes'

urlpatterns = [
    # Registro y Autenticación
    path('registro/', views.registro_contribuyente, name='registro_contribuyente'),
    path('dashboard/', views.dashboard_contribuyente, name='dashboard_contribuyente'),
    
    # URLs de autenticación estándar (opcional, si no las tienes)
    path('login/', auth_views.LoginView.as_view(template_name='contribuyentes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]