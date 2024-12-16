from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("books/", include("books.urls")),
    path("transactions/", include("transactions.urls")),
]
