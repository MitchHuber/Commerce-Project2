from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=20, default='IDK')

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    starting_bid = models.IntegerField()
    picture = models.URLField(null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"
