from django.db import models

# Create your models here.
# searchapp/models.py


class ArxivResult(models.Model):
    title = models.CharField(max_length=255)
    authors = models.TextField()
    abstract = models.TextField()
    arxiv_id = models.CharField(max_length=20, unique=True)
    published_date = models.DateTimeField()
    url = models.URLField(default="https://example.com")
    related = models.TextField(default="")

    def __str__(self):
        return self.title

    class Meta:
        app_label = "SearchEngine"


class SearchHistory(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} - {self.timestamp}"


# from django.contrib.auth.models import User

# class SearchHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     query = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.query}"
