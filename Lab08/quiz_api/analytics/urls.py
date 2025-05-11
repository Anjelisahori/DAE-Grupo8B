from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'question-stats', views.QuestionStatViewSet)
router.register(r'quiz-activities', views.QuizActivityViewSet)
router.register(r'user-quiz-attempts', views.UserQuizAttemptViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<int:pk>/analytics/', views.QuizAnalyticsView.as_view(), name='quiz-analytics'),
]