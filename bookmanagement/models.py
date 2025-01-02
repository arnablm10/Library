from django.db import models
from datetime import date

# Author Model
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def borrow(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
            return True
        return False

    def return_book(self):
        self.available_copies += 1
        self.save()


# BorrowRecord Model
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, related_name='borrow_records', on_delete=models.CASCADE)
    borrowed_by = models.CharField(max_length=255)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.borrowed_by} borrowed "{self.book.title}"'

    def mark_as_returned(self):
        self.return_date = date.today()
        self.book.return_book()  
        self.save()
