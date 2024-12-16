from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm


def home(request):
    if request.user.is_authenticated:
        return redirect("books:home")
    return render(request, "users/home.html")


def login_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in!")
        return redirect("books:home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfully logged in!")
            return redirect("books:home")
        else:
            messages.error(
                request,
                "Either the username or the password is wrong, please try again.",
            )
            return redirect("users:login")
    return render(request, "users/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("users:login")


def register_user(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in!")
        return redirect("books:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You are registered successfully!")
            return redirect("books:home")
        else:
            messages.error(
                request, "Something went wrong, check everything is correct again!"
            )
            return render(request, "users/register.html", {"form": form})
    form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def user_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access the page!")
        return redirect("users:login")
    borrowed_books =  request.user.borrowed_books.all()
    return render(
        request,
        "users/profile.html",
        {"user": request.user, "borrowed_books":borrowed_books},
    )
