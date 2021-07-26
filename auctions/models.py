from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.forms import ModelForm

# User, Listing, Watchlist, Bid, Comment

class User(AbstractUser):
    pass


class Listing(models.Model):

    CATEGORIES = [
        ("Vehicles", "Vehicles"),
        ("Fashion", "Fashion"),
        ("Books", "Books"),
        ("Electronics", "Electronics"),
        ("Collectibles & Art", "Collectibles & Art"),
        ("Home Appliances", "Home Appliances"),
        ("Toys & Hobbies", "Toys & Hobbies"),
        ("Health and Beauty", "Health and Beauty"),
        ("Uncategorized", "Uncategorized")
    ]

    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.FloatField(blank=True)
    category = models.CharField(max_length=18, choices=CATEGORIES)
    imgurl = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True) 
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user")

    def __str__(self):
        return f"{self.id}: {self.title}"


class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.watcher}: watching {self.listing.count()} listings"



class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="bidder")
    bid = models.FloatField()
    is_highest = models.BooleanField(default=False)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="commentedto")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="commenter")
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(blank=False)

    def __str__(self):
        return f"{self.commenter} commented on ({self.listing})"


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "creator")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("watcher",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "commenter", "date", "comment")
