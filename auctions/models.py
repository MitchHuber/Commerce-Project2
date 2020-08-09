from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length=20, default='None')

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    starting_bid = models.IntegerField()
    picture = models.URLField(null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} wants {self.item}"
