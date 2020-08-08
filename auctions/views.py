from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import User, Categories, Listings


def index(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('starting_price')
        pic = request.POST.get('picture')
        category = request.POST.get('category')
        cat = Categories.objects.get(category=category)

        # If the user doesnt include a photo, a stock image is used
        if not pic:
            pic = "https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483141.jpg"
        # Checks to make sure user includes a title, description, & price.
        if not title or not description or not price:
            message = "You must include a title, description, & price."
            return render(request, "auctions/create_listing.html", {
                "message": message,
                "categories": Categories.objects.all()
            })

        #Create listing
        listing = Listings(
            title = title,
            description = description,
            starting_bid = price,
            picture =  pic,
            category = cat
        )

        listing.save()

        return render(request, "auctions/index.html",{
            "listings": Listings.objects.all()
        })
    #Get request, passes all the listings
    else:
        return render(request, "auctions/index.html",{
            "listings": Listings.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    #links user to the webpage to create a new listing
    return render(request, "auctions/create_listing.html", {
        "categories": Categories.objects.all()
    })

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    #Links user to the webpage that displays all of the categories
    return render(request, "auctions/categories.html",{
        "categories": Categories.objects.all()
    })

def category(request, cat):
    #Create a list for listings with a specific category
    list = []
    items = Listings.objects.all()

    #Checks between the category selcted and the listing's category
    for item in items:
        if item.category == Categories.objects.get(category=cat):
            list.append(item)
    #Path if chosen category has no listings
    if len(list) == 0:
        return render(request, "auctions/categories.html",{
            "message": f"There are no items in the {cat} category."
        })
    return render(request, "auctions/category.html", {
        "items": list
    })

def item(request, title):
    if request.method == "POST":
        item = Listings.objects.get(title=title)
        bid = request.POST.get('bid')

        if(int(bid) <= item.starting_bid):
            message = "Your bid must be greater than the current bid."
            return render(request, "auctions/item.html",{
                "message": message, "title": item.title, "price": item.starting_bid,
                "description": item.description, "picture": item.picture,
                "category": item.category
            })
        else:
            item.starting_bid = bid
            item.save()
            message = "Your bid was successful!"
            return render(request, "auctions/item.html",{
                "message": message, "title": item.title, "price": item.starting_bid,
                "description": item.description, "picture": item.picture,
                "category": item.category
            })
    else:
        if title == "admin":
            return HttpResponseRedirect(reverse('admin:index'))
        else:
            item = Listings.objects.get(title=title)
            title = item.title
            price = item.starting_bid
            description = item.description
            pic = item.picture
            category = item.category

            return render(request, "auctions/item.html",{
                "title": title, "price": price, "description": description,
                "picture": pic, "category": category
            })
