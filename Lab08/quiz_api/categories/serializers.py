from rest_framework import serializers
from .models import Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    """Serializador para el modelo Category."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tag."""
    class Meta:
        model = Tag
        fields = ['id', 'name']

