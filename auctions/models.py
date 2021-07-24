from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model

# User, Listing, Watchlist, Bid, Comment

class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64)
    imgurl = models.TextField()
    date = models.CharField(max_length=10)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f"{self.id}: {self.title}"


class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.user} watches {self.listing}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bod = models.FloatField()


class Comment(models.Model):
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    date = models.CharField(max_length=10)
    comment = models.TextField()

