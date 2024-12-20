from django.db import models
from Student_app.models import Program, Branch, Teacher, Subject, Student, Book_Type
import uuid



class Book(models.Model):

    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField()
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    borrowed_by = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="book_covers/")
    description = models.TextField()

    def __str__(self):
        return self.book_title
    

    

class BookAssignment(models.Model):

    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name='book_assign')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='book_assign')
    semester = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='book_assign')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book_assign')
    date_of_assignment = models.DateField(auto_now_add=True)
    number_of_copies = models.PositiveIntegerField(default=1)
    date_of_submission = models.DateField()

    def __str__(self):
        return f"{self.book.book_title} assigned to {self.student.name}"