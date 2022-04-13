from django.db import models
from .user import User

class Paper(models.Model):
    """

    Fields:
        - title: paper title
        - url: to which the paper content should be seen
        - abstract: paper abstract
        - export_bib: the bibtex format string when this paper is exported as reference
    """
    title = models.CharField(max_length=100)
    url = models.URLField()
    abstract = models.CharField(max_length=1000)
    export_bib = models.CharField(max_length=500)  # tobe confirmed TODO
    authors = models.ManyToManyField(User, related_name='papers')
    