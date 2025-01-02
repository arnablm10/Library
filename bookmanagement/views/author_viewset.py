from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from bookmanagement.models import Author
from bookmanagement.serializers.author_serializer import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]