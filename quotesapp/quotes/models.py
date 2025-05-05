from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    full_name     = models.CharField(max_length=50, null=False, unique=True)
    born_date     = models.CharField(max_length=25, null=False)
    born_location = models.CharField(max_length=100, null=False)
    description   = models.TextField(null=False)

    def __str__(self):
        return f"{self.full_name}"


class Quote(models.Model):
    quote  = models.TextField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags   = models.ManyToManyField(Tag)

    def __str__(self):
        return f"'{self.quote[:50]}...', {self.author}"
