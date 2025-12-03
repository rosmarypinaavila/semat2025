from django.urls import path
from  .views import *
from act_econ import views

urlpatterns = [
    path('act_econ/', views.listar_empresas_contribuyente, name='listar_empresas_contribuyente'),
]