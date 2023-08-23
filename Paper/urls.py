# searchapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("<id>", views.chatpaper, name="chatpaper"),
]
