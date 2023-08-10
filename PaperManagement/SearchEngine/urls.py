# searchapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.search_arxiv, name='search_arxiv'),
    #path('search_page/', views.search_page, name='search_page'),
    path('api/recommended/', views.recommended_papers, name='recommended_papers'),
]
