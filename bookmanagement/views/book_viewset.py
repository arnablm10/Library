# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from bookmanagement.models import Book
from bookmanagement.serializers.book_serializer import BookSerializer
from bookmanagement.models import Author

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        TITLE = request.data.get("title", None)
        AUTHOR_ID = request.data.get("author_id", None)
        ISBN = request.data.get("isbn", None)
        AVAILABLE_COPIES = request.data.get("available_copies", 0)

        if not TITLE or not AUTHOR_ID or not ISBN:
            return Response({"detail: Incomplete data provided for the book"}, status=status.HTTP_400_BAD_REQUEST)
        
        # add any isbn validation function if required
        try:
            AUTHOR = Author.objects.get(id = AUTHOR_ID)
        except Author.DoesNotExist:
            return Response({"detail": "Author of the book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        NEW_BOOK = Book.objects.create(
                    title = TITLE,
                    isbn = ISBN,
                    available_copies = AVAILABLE_COPIES,
                    author = AUTHOR
                    )
        NEW_BOOK.save()

        return Response(BookSerializer(NEW_BOOK).data, status=status.HTTP_201_CREATED)






