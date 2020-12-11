from .models import Question, Choice
from rest_framework import serializers

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    books = ChoiceSerializer(read_only=True,many=True)
    class Meta:
        model = Question
        fields = '__all__'
