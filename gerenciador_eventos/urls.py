
from django.urls import path, include

urlpatterns = [
    
    path('api/', include('eventos.urls')),  # Inclui as rotas do app eventos
]
