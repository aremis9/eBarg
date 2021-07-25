from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from .models import *
# User, Listing, Watchlist, Bid, Comment


CATEGORIES = [
    "Vehicles",
    "Fashion",
    "Books",
    "Electronics",
    "Collectibles & Art",
    "Home Appliances",
    "Toys & Hobbies",
    "Health and Beauty",
    "Uncategorized"
]

NOIMAGE = 'http://www.jazzmusicarchives.com/images/covers/quantic(united-kingdom)-the-sheepskin-sessions-20210219105013.jpg'

def index(request):
    listing = Listing.objects.order_by('date')
    return render(request, "auctions/index.html", {
        'user': request.user,
        'listing': listing,
        'image': 'https://qph.fs.quoracdn.net/main-qimg-06697523db4cb85b25b8cf1ce95f2d4e'
    })


def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not email or not username or not password or not confirmation:
            return render(request, "auctions/register.html", {
                "message": "All fields are required.",
                'email': email,
                'username': username
            })

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords don\'t match",
                'email': email,
                'username': username
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/register.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


def category(request, category):
    listing = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listing": listing
    })


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    return render(request, "auctions/listing.html", {
        'listing': listing
    })


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        imgurl = request.POST["imgurl"]
        creator = User.objects.get(username=request.user)

        try:
            price = float(price)
        except:
            return render(request, "auctions/create.html", {
                "message": "Invalid Starting Price",
                "categories": CATEGORIES,
                "title": title,
                "description": description,
                "imgurl": imgurl,
            })

        if not title or not description or not category or not price:
            return render(request, "auctions/create.html", {
                "message": "Input required fields.",
                "categories": CATEGORIES,
                "title": title,
                "description": description,
                "imgurl": imgurl,
                "price": price
            })

        if category not in CATEGORIES:
            return render(request, "auctions/create.html", {
                "message": "Invalid Category",
                "categories": CATEGORIES,
                "title": title,
                "description": description,
                "imgurl": imgurl
            })

        if not imgurl:
            imgurl = NOIMAGE

        
        new_listing = Listing(
            title=title,
            description=description,
            price=price,
            category=category,
            imgurl=imgurl,
            creator=creator
        )

        new_listing.save()

        return HttpResponseRedirect('/')


    else:
        return render(request, "auctions/create.html", {
            "categories": CATEGORIES
        })