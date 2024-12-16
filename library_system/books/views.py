from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Book, Instance, Author
from django.utils.http import url_has_allowed_host_and_scheme


def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    query = request.GET.get("q", "")
    if query:
        books = Book.objects.filter(
            Q(name__icontains=query) | Q(author__name__icontains=query)
        )
    else:
        books = Book.objects.all()
    for book in books:
        book.is_borrowed = Instance.objects.filter(
            user=request.user, book=book
        ).exists()
    return render(request, "books/home.html", context={"query": query, "books": books})


def borrow_book(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "POST":
        next_url = request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts=request.get_host()
        ):
            return redirect("books:home")
        user = request.user
        try:
            book = Book.objects.get(id=pk)
        except:
            messages.error(request, "The book was not found!")
            return redirect(next_url)
        if Instance.objects.filter(book=book).exists():
            messages.error(request, "You have already borrowed the book!")
            return redirect(next_url)
        if book.books_left <= 0:
            messages.error(request, "Sorry, all instances of this book are borrowed!")
            return redirect(next_url)
        try:
            days = int(request.POST.get("days"))
            if days <= 0:
                raise ValueError
        except:
            messages.error(request, "Invalid number of days, try again!")
            return redirect(next_url)
        book.books_left -= 1
        book.save()
        instance = Instance.objects.create(book=book, user=user, days_borrowed=days)
        bill = book.price * days
        user.profile.total_bill += bill
        user.profile.save()
        messages.success(
            request,
            f"{book} successfully borrowed for {days} day(s)! Your bill for this transaction is Rs. {bill}",
        )
        return redirect(next_url)
    messages.error(request, "You are not allowed to access the page!")
    return redirect("books:home")

def return_book(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "POST":
        next_url = request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(
            next_url, allowed_hosts=request.get_host()
        ):
            return redirect("books:home")
        user = request.user
        try:
            book = Book.objects.get(id=pk)
        except:
            messages.error(request, "The book was not found!")
            return redirect(next_url)
        try:
            instance = Instance.objects.get(user=user, book=book)
        except:
            messages.error(request, "You have not borrowed this book!")
            return redirect(next_url)
        instance.delete()
        book.books_left += 1
        book.save()
        messages.success(request, f"{book} successfully returned!")
        return redirect(next_url)
    messages.error(request, "You are not allowed to access the page!")
    return redirect("books:home")


def book_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "GET":
        try:
            book = Book.objects.get(id=pk)
        except:
            messages.error(request, "The book was not found!")
            return redirect("books:home")
        borrowed = Instance.objects.filter(user=request.user, book=book).exists()
        return render(
            request, "books/book_view.html", {"borrowed": borrowed, "book": book}
        )


def author_view(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    if request.method == "GET":
        try:
            author = Author.objects.get(id=pk)
        except:
            messages.error(request, "The authior does not exist!")
            return redirect("books:home")
        books = Book.objects.filter(author=author)
        for book in books:
            book.is_borrowed = Instance.objects.filter(
                user=request.user, book=book
            ).exists()
        return render(
            request, "books/author_view.html", {"author": author, "books": books}
        )
