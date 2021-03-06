from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from .models import *
import json
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
    listing = Listing.objects.order_by('date').filter(isactive=True)
    listings = {}
    for l in listing:
        listings[l] = Bid.objects.filter(listing=l.pk).latest('bid').bid

    return render(request, "auctions/index.html", {
        'user': request.user,
        'listings': listings,
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
        
        create_watchlist = Watchlist(
            watcher=user,
        )

        create_watchlist.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/register.html")


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


def category(request, category):
    listing = Listing.objects.order_by('date').filter(isactive=True, category=category)
    listings = {}
    for l in listing:
        listings[l] = Bid.objects.filter(listing=l.pk).latest('bid').bid
        
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })


def listing0(request):
    return HttpResponseRedirect('/')


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    message = ''
    comments = list(Comment.objects.filter(listing=id))
    if request.method == "POST":
        if 'user' and 'listing' in request.POST:
            username = request.POST["user"]
            listing_id = request.POST["listing"]

            watcher = User.objects.get(username=username)
            watching = Listing.objects.get(pk=listing_id)

            if watching != listing:
                status = 'not added'
                return HttpResponse(json.dumps(status))


            if watcher.pk not in Watchlist.objects.values_list('watcher', flat=True):
                addwatchlist = Watchlist(
                    watcher=watcher,
                )

                addwatchlist.save()


            watchlist = Watchlist.objects.get(watcher=watcher.pk)
            if watching.pk in list(Watchlist.objects.filter(watcher=watcher.pk).values_list('listing', flat=True)):
                is_watching = False
                watchlist.listing.remove(watching.pk)
            else:
                is_watching = True
                watchlist.listing.add(watching.pk)

            return HttpResponse(json.dumps(is_watching))

        elif 'bid' in request.POST:
            bid = request.POST['bid']
            bidder = User.objects.get(username=request.user)

            try:
                bid = float(bid)
            except ValueError:
                message = 'Invalid Bid!'

            if message != 'Invalid Bid!':
                highest = Bid.objects.latest('bid')
                bidrule = '''The bid must be greater than the current highest bid'''
                if listing.price == highest.bid:
                    if bid >= listing.price:
                        pass
                    else:
                        message = bidrule
                if bid >= listing.price and bid > highest.bid:
                    pass
                else:
                    message = bidrule
                
                if message != bidrule:

                    addbid = Bid(
                        listing=listing,
                        bidder=bidder,
                        bid=bid,
                    )

                    addbid.save()

        elif 'comment' in request.POST:
            commenter = User.objects.get(username=request.user)
            comment = request.POST['comment']

            if not comment:
                message = 'Comment must not be empty!'
            else:
                addcomment = Comment(
                    listing=listing,
                    commenter=commenter,
                    comment=comment
                )

                addcomment.save()
                
                comments.append(addcomment)
        
        elif 'closebid' in request.POST:
            listing.isactive = False
            listing.save()


    if request.user.is_authenticated:
        userpk = User.objects.get(username=request.user).pk
        userwatchlist = list(Watchlist.objects.filter(watcher=userpk).values_list('listing', flat=True))
        if id in userwatchlist:
            is_watching = True
        else:
            is_watching = False
    else:
        is_watching = False

    highestbid = Bid.objects.filter(listing=id).latest('bid')

    return render(request, "auctions/listing.html", {
        'message': message,
        'listing': listing,
        'highestbid': highestbid,
        'is_watching': is_watching,
        'comments': comments
    })


@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"].replace(',', '')
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


        current_price = Bid(
            listing=new_listing,
            bidder=creator,
            bid=price
        )

        current_price.save()

        return HttpResponseRedirect('/listing/' + str(new_listing.pk))


    else:
        return render(request, "auctions/create.html", {
            "categories": CATEGORIES
        })


@login_required()
def watchlist(request):
    userpk = User.objects.get(username=request.user).pk
    listings = list(Watchlist.objects.get(watcher=userpk).listing.all())
    # .values_list('listing', flat=True)
    # watchlist = Listing.objects
    return render(request, "auctions/watchlist.html", {
        "listing": listings
    })
