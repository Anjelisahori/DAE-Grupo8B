from rest_framework import serializers
from .models import QuestionStat, QuizActivity, UserQuizAttempt

class QuestionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionStat
        fields = '__all__'  # Or specify fields like ['question', 'attempts', 'correct_attempts', 'success_rate']

class QuizActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizActivity
        fields = '__all__' # Or specify fields

class UserQuizAttemptSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Display username, not ID

    class Meta:
        model = UserQuizAttempt
        fields = '__all__'