from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, QuizAttempt

class UserSerializer(serializers.ModelSerializer):
    """Serializador para el modelo User."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Incluye los campos que necesites

class ProfileSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Profile."""
    user = UserSerializer(read_only=True)  # Serializa la información del usuario anidada
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar']

class QuizAttemptSerializer(serializers.ModelSerializer):
    """Serializador para el modelo QuizAttempt."""
    user = UserSerializer(read_only=True)
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)  # Opcional, si quieres detalles del quiz usa QuizSerializer de la app quizzes
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'max_score', 'completed_at']

