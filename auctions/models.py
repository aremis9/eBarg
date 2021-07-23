from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    '''
        Watchlist
    '''
    pass


class Listing(models.Model):
    '''
        Creator
        Title
        Description
        Category
        Image
    '''
    pass


class Bid(models.Model):
    '''
        Bid (Highest bid = current price of listing)
        Bidder
    '''
    pass


class Comment(models.Model):
    '''
        Username
        Date
        Comment
    '''
    pass