from django.urls import path, include
from . import views

app_name = "books"
urlpatterns = [
    path("", views.home, name="home"),
    path("borrow_book/<int:pk>/", views.borrow_book, name="borrow_book"),
    path("return_book/<int:pk>/", views.return_book, name="return_book"),
]
