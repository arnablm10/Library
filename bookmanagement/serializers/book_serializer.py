# serializers.py
from .author_serializer import AuthorSerializer
from rest_framework import serializers
from bookmanagement.models import Book

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # Nested Author Serializer

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'available_copies']
