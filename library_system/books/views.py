from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Instance, Author


def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    books = Book.objects.all()
    for book in books:
        book.is_borrowed = Instance.objects.filter(user=request.user, book=book).exists()
    return render(request, "books/home.html", context={'books' : books})


def borrow_book(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "POST":
        user = request.user
        try:
            book = Book.objects.get(id=pk)
        except:
            messages.error(request, "The book was not found!")
            return redirect("books:home")
        if Instance.objects.filter(book=book).exists():
            messages.error(request, "You have already borrowed the book!")
            return redirect("books:home")
        if book.books_left <= 0:
            messages.error(request, "Sorry, all instances of this book are borrowed!")
            return redirect("books:home")
        try:
            days = int(request.POST.get("days"))
            if days <= 0:
                raise ValueError
        except:
            messages.error(request, "Invalid number of days, try again!")
            return redirect("books:home")
        book.books_left -= 1
        book.save()
        instance = Instance.objects.create(book=book, user=user, days_borrowed=days)
        user.profile.total_bill += book.price * days
        user.profile.save()
        return redirect("books:home")


def return_book(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "POST":
        user = request.user
        try:
            book = Book.objects.get(id=pk)
        except:
            messages.error(request, "The book was not found!")
            return redirect("books:home")
        try:
            instance = Instance.objects.get(user=user, book=book)
        except:
            messages.error(request, "You have not borrowed this book!")
            return redirect("books:home")
        instance.delete()
        book.books_left += 1
        book.save()
        return redirect("books:home")
