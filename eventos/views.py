from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .models import Evento, CustomUser
from .serializer import EventoSerializer, UserSerializer, LoginSerializer, InscricaoSerializer
from django.http import HttpResponse


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def listar_eventos(request):
    if request.method == 'GET':
        eventos = Evento.objects.all()
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:  
            return Response({'detail': 'Você não tem permissão para criar eventos.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])  
def atualizar_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'detail': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EventoSerializer(evento, data=request.data)
    elif request.method == 'PATCH':
        serializer = EventoSerializer(evento, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deletar_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'detail': 'Evento não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    evento.delete()
    return Response({'detail': 'Evento deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)



class RegistroUsuario(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer



class LoginUsuario(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })



class EventoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class ListarEventos(generics.GenericAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    pagination_class = EventoPagination

    def get(self, request, *args, **kwargs):
        eventos = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(eventos, request)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def inscrever_evento(request):
    serializer = InscricaoSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Inscrição realizada com sucesso!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return HttpResponse("Bem-vindo ao Sistema de Eventos!")
