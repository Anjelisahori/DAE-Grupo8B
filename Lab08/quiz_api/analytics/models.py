from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Important: Use Django's built-in User model

class QuestionStat(models.Model):
    question = models.ForeignKey('quizzes.Question', on_delete=models.CASCADE, related_name='stats')
    attempts = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)

    @property
    def success_rate(self):
        return (self.correct_attempts / self.attempts) * 100 if self.attempts > 0 else 0

    def __str__(self):
        return f"Stats for: {self.question.text[:30]}..."

class QuizActivity(models.Model):
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE, related_name='activities')
    date = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    starts = models.IntegerField(default=0)
    completions = models.IntegerField(default=0)

    class Meta:
        unique_together = ['quiz', 'date']  # Ensure only one entry per quiz per day

    def __str__(self):
        return f"{self.quiz.title} activity on {self.date}"

class UserQuizAttempt(models.Model):  # Model to track user-specific quiz attempts
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.CASCADE)
    score = models.IntegerField()
    max_score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.score}/{self.max_score}"