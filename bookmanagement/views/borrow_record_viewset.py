# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from django.db import transaction
from bookmanagement.models import BorrowRecord, Book
from bookmanagement.serializers.borrow_record_serializer import BorrowRecordSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        BOOK_ID = request.data.get('book_id', None)
        BORROWER = request.data.get('borrowed_by', None)
        if not BOOK_ID or not BORROWER:
            return Response({"detail: Incomplete api request"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            BOOK = Book.objects.get(id=BOOK_ID)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if BorrowRecord.objects.filter(book=BOOK, borrowed_by=BORROWER, return_date__isnull = True).exists():
            return Response({"detail": "Book already borrowed. Not returned"}, status=status.HTTP_400_BAD_REQUEST)

        
        if BOOK.borrow():
            borrow_record = BorrowRecord.objects.create(
                book=BOOK,
                borrowed_by=request.data.get('borrowed_by')
            )

            return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)
        
        return Response({'detail': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    # Custom `update` method for returning a book
    @transaction.atomic
    @action(detail=True, methods=['put'], url_path="return")
    def return_book(self, request, *args, **kwargs):
        borrow_record = self.get_object()
        if borrow_record.return_date:
            return Response({"detail": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST)
        
        borrow_record.mark_as_returned()        

        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_200_OK)
