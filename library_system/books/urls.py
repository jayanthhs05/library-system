from django.urls import path, include
from . import views

app_name = "books"
urlpatterns = [
    path("", views.home, name="home"),
    path("borrow_book/<int:pk>/", views.borrow_book, name="borrow_book"),
    path("return_book/<int:pk>/", views.return_book, name="return_book"),
    path("book/<int:pk>/", views.book_view, name="book_view"),
    path("author/<int:pk>/", views.author_view, name="author_view")
]
