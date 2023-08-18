from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/register/", views.register_view, name="register"),
    path("auth/logout/", views.logout_view, name="logout"),
]
