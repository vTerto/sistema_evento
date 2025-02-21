from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Modelo CustomUser já existente
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    inscricoes = models.ManyToManyField('Evento', blank=True)
    pass

User=get_user_model()

class Evento(models.Model):
    nome = models.CharField(max_length=255)
    data = models.DateTimeField()
    local = models.CharField(max_length=255)
    descricao = models.TextField()
    inscritos = models.ManyToManyField(User, related_name="eventos_inscritos")  # Adicione related_name

    def __str__(self):
        return self.nome
