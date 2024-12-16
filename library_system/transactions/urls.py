from django.urls import path
from . import views

app_name = "transactions"
urlpatterns = [
    path("", views.home, name="home"),
    path("payment", views.payment, name="payment"),
]
