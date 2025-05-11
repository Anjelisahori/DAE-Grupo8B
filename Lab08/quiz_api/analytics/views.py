from django.shortcuts import render
from rest_framework import viewsets, generics, views, response, status
from .models import QuestionStat, QuizActivity, UserQuizAttempt
from .serializers import QuestionStatSerializer, QuizActivitySerializer, UserQuizAttemptSerializer
from quizzes.models import Quiz  # Import Quiz model
from rest_framework.permissions import IsAuthenticatedOrReadOnly # Example permission

class QuestionStatViewSet(viewsets.ModelViewSet):
    queryset = QuestionStat.objects.all()
    serializer_class = QuestionStatSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Example - adjust as needed

class QuizActivityViewSet(viewsets.ModelViewSet):
    queryset = QuizActivity.objects.all()
    serializer_class = QuizActivitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserQuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = UserQuizAttempt.objects.all()
    serializer_class = UserQuizAttemptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically associate the current user

class QuizAnalyticsView(generics.RetrieveAPIView):  # Example of a custom analytics view
    queryset = Quiz.objects.all()
    serializer_class = QuizActivitySerializer  # Or create a combined serializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        # Get or create QuizActivity for today
        activity, created = QuizActivity.objects.get_or_create(quiz=quiz, date=models.DateField.today())
        activity.views += 1
        activity.save()

        serializer = self.get_serializer(activity)
        return response.Response(serializer.data)
