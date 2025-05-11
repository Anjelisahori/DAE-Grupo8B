from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly # Ejemplo de permiso
from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Ejemplo: Cualquiera puede leer, pero solo autenticados pueden crear/editar/borrar

class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


