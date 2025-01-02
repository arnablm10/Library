from rest_framework.test import APITestCase
from rest_framework import status
from bookmanagement.models import Book, BorrowRecord, Author
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class BorrowRecordReturnTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.borrower_name = "test_borrower"
        # Create a book with available copies
        self.author = Author.objects.create(name = "Test Author", bio = "sports stories writer")
        self.book = Book.objects.create(
            title="Test Book", author=self.author, isbn="1234567890123", available_copies=5
        )
        # Create a borrow record
        self.borrow_record = BorrowRecord.objects.create(
            book=self.book,
            borrowed_by=self.borrower_name,
        )

        self.headers = {'Authorization': f'Bearer {self.token}'}

    '''
    testing 'borrow/:borrowRecordId/return' 
    So 5 copies -> 6 copies
    '''
    def test_mark_book_as_returned(self):
        # URL for returning a book
        url = f'/borrow/{self.borrow_record.id}/return/'
        # Send a PUT request to mark the book as returned
        response = self.client.put(url, {}, format='json', HTTP_AUTHORIZATION=self.headers['Authorization'])

        # Check that the response status code is HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the return_date has been set
        self.borrow_record.refresh_from_db()
        self.assertIsNotNone(self.borrow_record.return_date)
        
        # Check if the available copies of the book have increased by 1
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 6)  # One copy has been returned


    '''
    testing 'borrow'
    So 6 copies -> 5 copies
    '''
    def test_borrow_records(self):
        url = '/borrow/'
        data = {"borrowed_by": "Federico Dimarco",
                "book_id": self.book.id}
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=self.headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.book.available_copies, 5)