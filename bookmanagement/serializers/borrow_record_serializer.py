# serializers.py
from rest_framework import serializers
from .book_serializer import BookSerializer
from bookmanagement.models import BorrowRecord

class BorrowRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Nested Book Serializer
    borrowed_by = serializers.CharField(max_length=255)  # Borrower's name as a simple field
    return_date = serializers.DateField(required=False, allow_null=True) # making the field optional in json

    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrowed_by', 'borrow_date', 'return_date']
