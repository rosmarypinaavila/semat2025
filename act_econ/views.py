from django.shortcuts import render

# Create your views here.


def empresas(request):
    return render(request, 'actecon/empresas.html')