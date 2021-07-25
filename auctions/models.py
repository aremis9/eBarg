from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.forms import ModelForm

# User, Listing, Watchlist, Bid, Comment

class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField(blank=True)
    category = models.CharField(max_length=64)
    imgurl = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user")

    def __str__(self):
        return f"{self.id}: {self.title}"


class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.user} watches {self.listing}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="bidder")
    bid = models.FloatField()
    is_highest = models.BooleanField(default=False)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="commentedto")
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="commentor")
    date = models.DateField(auto_now_add=True)
    comment = models.TextField()

