from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/register/", views.register_view, name="register"),
    path("auth/logout/", views.logout_view, name="logout"),
    path('update-domains/', views.update_domains, name='update-domains'),
]
