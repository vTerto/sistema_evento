from django.urls import path
from .views import (
    listar_eventos, 
    atualizar_evento, 
    deletar_evento, 
    RegistroUsuario, 
    LoginUsuario, 
    inscrever_evento  # Nome correto aqui (antes estava InscreverEvento)
)

urlpatterns = [
    path('eventos/', listar_eventos, name='listar_eventos'),
    path('eventos/<int:pk>/', atualizar_evento, name='atualizar_evento'),
    path('eventos/<int:pk>/deletar/', deletar_evento, name='deletar_evento'),
    path('auth/registro/', RegistroUsuario.as_view(), name='registro_usuario'),
    path('auth/login/', LoginUsuario.as_view(), name='login_usuario'),
    path('eventos/inscrever/', inscrever_evento, name='inscrever_evento'),  # Corrigido!
]
