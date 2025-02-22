
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Bem-vindo ao Sistema de Eventos!")

urlpatterns = [
    path('', home, name='home'),
    path('api/', include('eventos.urls')),  # Inclui as rotas do app eventos
]
