from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser # Ejemplo de permisos
from django.contrib.auth.models import User
from .models import Profile, QuizAttempt
from .serializers import UserSerializer, ProfileSerializer, QuizAttemptSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para el modelo User.  Solo lectura, ya que la creación de usuarios
    generalmente se maneja con un formulario de registro o una vista personalizada.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Solo el administrador puede listar usuarios

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden ver/editar su perfil

    def get_object(self):
        """
        Permite a un usuario obtener SÓLO su propio perfil.
        """
        pk = self.kwargs.get('pk')
        if pk == 'current':
            return self.request.user.profile
        return super().get_object()

    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Endpoint para obtener el perfil del usuario actual.
        """
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)


class QuizAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para el modelo QuizAttempt.
    """
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden ver sus intentos

    def get_queryset(self):
        """
        Filtra los intentos de quiz para que un usuario solo vea los suyos.
        El administrador puede ver todos.
        """
        if self.request.user.is_staff:
            return super().get_queryset()
        return QuizAttempt.objects.filter(user=self.request.user)

