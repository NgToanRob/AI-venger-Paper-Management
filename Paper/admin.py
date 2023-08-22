from django.contrib import admin

from .models import Author, Paper

admin.site.register(Paper)
admin.site.register(Author)
