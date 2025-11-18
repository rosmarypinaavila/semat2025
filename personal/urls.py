from django.urls import path
from  .views import *
from personal import views


urlpatterns = [
    path('home', home, name='home'),
] 