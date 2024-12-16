from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField(default="")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    books_left = models.IntegerField()

    def __str__(self):
        return f"{self.name} by {self.author.name}"


class Instance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowed_books"
    )
    days_borrowed = models.IntegerField()

    def __str__(self):
        return f"{self.book.name} with {self.user.username}"
