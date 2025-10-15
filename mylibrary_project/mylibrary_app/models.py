from django.db import models
from django.utils import timezone


# Student model (acts like user)
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    roll_number = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Student'

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


# Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Book'

    def __str__(self):
        return f"{self.title} by {self.author}"


# IssueBook model
class IssueBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        db_table = 'IssueBook'

    def __str__(self):
        return f"{self.student.name} → {self.book.title}"