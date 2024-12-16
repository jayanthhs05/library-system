from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.user_profile, name="profile"),
]
