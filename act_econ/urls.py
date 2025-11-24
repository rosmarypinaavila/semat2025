from django.urls import path
from  .views import *
from act_econ import views

urlpatterns = [
    path('/empresas/', empresas),
    
] 