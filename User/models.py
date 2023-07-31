from django.db import models
from Paper.models import Author, Paper


class User(models.Model):
    name = models.CharField(max_length=100)  # Username
    research_interests = models.CharField(max_length=200)  # Research areas of user interest, e.g. NLP, Computer Vision
    subscribed_journals = models.CharField(max_length=200)  # The journals the user subscribes to
    favorite_authors = models.ManyToManyField(Author, blank=True)  # Authors that the user is interested in and follows
    saved_papers = models.ManyToManyField(Paper, blank=True)  # List of papers that the user has saved or bookmarked

    def __str__(self):
        return self.name