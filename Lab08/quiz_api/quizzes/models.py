from django.db import models

# Asegúrate de importar los modelos Category y Tag
from categories.models import Category, Tag


class Quiz(models.Model):
    """Model for quizzes"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Añadimos la relación con Category
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, null=True, related_name='quizzes')

    # Añadimos la relación con Tag
    tags = models.ManyToManyField('categories.Tag', related_name='quizzes', blank=True)

    class Meta:
        verbose_name_plural = "quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """Model for questions within a quiz"""
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text


class Choice(models.Model):
    """Model for answer choices for a question"""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text
