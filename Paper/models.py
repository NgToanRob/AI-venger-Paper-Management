from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)  # Name of the author

    def __str__(self):
        return self.name


class Paper(models.Model):
    # title = models.CharField(max_length=200)  # The title of the paper
    # authors = models.ManyToManyField(Author)  # Many-to-many relationship with Authors model
    # publication_date = models.DateField()  # The publication date of the paper
    # abstract = models.TextField()  # Summary of the content of the paper
    # domain = models.CharField(max_length=50)  # Research area of the paper (e.g., NLP, Computer Vision)
    # pdf_url = models.URLField()  # The path to the PDF file of the paper
    # references = models.ManyToManyField('self', blank=True, symmetrical=False)  # List of reference Papers
    # conference_journal = models.CharField(max_length=100)  # Name of conference or journal
    # rank = models.IntegerField(null=True, blank=True)  # Rank of the paper (optional)
    content = models.TextField()

    def __str__(self):
        return self.title
