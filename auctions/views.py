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
    return render(request, "auctions/create_listing.html", {
        "categories": Categories.objects.all()
    })

def item(request, title):

        item = Listings.objects.get(title=title)
        title = item.title
        price = item.starting_bid
        description = item.description
        pic = item.picture
        category = item.category
        print(item)
        return render(request, "auctions/item.html",{
            "title": title, "price": price, "description": description,
            "picture": pic, "category": category
        })
