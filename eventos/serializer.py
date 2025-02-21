from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Evento, CustomUser

# Serializador de Evento
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

# Serializador de Usuário (CustomUser)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'is_staff']  # Incluí `is_staff` para diferenciar admin e usuário comum
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)  # Alterado para CustomUser
        return user

# Serializador de Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Usuário ou senha incorretos.')
        data['user'] = user
        return data

# Serializador de Inscrição em Evento
class InscricaoSerializer(serializers.Serializer):
    evento_id = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user  # Obtém o usuário autenticado
        evento_id = data.get('evento_id')

        # Verifica se o evento existe
        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            raise serializers.ValidationError({'evento_id': 'Evento não encontrado.'})

        # Verifica se o usuário já está inscrito
        if evento.inscritos.filter(id=user.id).exists():
            raise serializers.ValidationError({'evento_id': 'Você já está inscrito neste evento.'})

        data['evento'] = evento
        return data

    def create(self, validated_data):
        evento = validated_data['evento']
        user = self.context['request'].user
        evento.inscritos.add(user)  # Adiciona o usuário à lista de inscritos do evento
        return validated_data
