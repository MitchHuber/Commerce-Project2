from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import User, Categories, Listings, Watchlist, Bids, Comments, ListingsWon


def index(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('starting_price')
        pic = request.POST.get('picture')
        category = request.POST.get('category')
        cat = Categories.objects.get(category=category)
        owner = User.objects.get(username=request.user)

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
            category = cat,
            owner = owner
        )

        listing.save()

        return render(request, "auctions/index.html",{
            "listings": Listings.objects.all()
        })
    #Get request, passes all the listings
    else:
        won = False
        wins = ListingsWon.objects.all()
        for listing in wins:
            if listing.user == request.user:
                won = True
        return render(request, "auctions/index.html",{
            "listings": Listings.objects.all(), "won": won
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
    won = False
    wins = ListingsWon.objects.all()
    for listing in wins:
        if listing.user == request.user:
            won = True
    return render(request, "auctions/create_listing.html", {
        "categories": Categories.objects.all(), "won": won
    })

def watchlist(request):
    won = False
    wins = ListingsWon.objects.all()
    watchlist = Watchlist.objects.all()
    list = []

    for listing in watchlist:
        if listing.user == User.objects.get(username=request.user):
            list.append(listing.item)

    for listing in wins:
        if listing.user == request.user:
            won = True

    if len(list) == 0:
        return render(request, "auctions/category.html",{
            "message": "There are no items in your watchlist.", "won": won
            })
    else:
        return render(request, "auctions/category.html",{
            "items": list, "won":won
        })

def addwatchlist(request, title):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        item = Listings.objects.get(title=title)
        isowner = False
        won = False

        wins = ListingsWon.objects.all()
        for listing in wins:
            if listing.user == request.user:
                won = True

        watchlist = Watchlist(
            user = user,
            item = item
        )

        watchlist.save()
        if item.owner == request.user:
            isowner = True

        comments = Comments.objects.all()
        commentList = []
        for comment in comments:
            if comment.item == item:
                commentList.append(comment)

        try:
            bid = Bids.objects.get(user=request.user,item=item)
            if bid.price == item.starting_bid:
                highestBidder = True
            return render(request,"auctions/item.html",{
                "title": item.title, "price": item.starting_bid, "description": item.description,
                "picture": item.picture, "category": item.category, "check": True, "owner": item.owner,
                "highestBidder": highestBidder, "isowner": isowner, "comments": commentList, "won": won
            })
        except:
            return render(request, "auctions/item.html",{
            "title": item.title, "price": item.starting_bid, "description": item.description,
            "picture": item.picture, "category": item.category, "check": True, "owner": item.owner,
            "isowner": isowner, "comments": commentList, "won": won
            })

def removewatchlist(request, title):
    user = User.objects.get(username=request.user)
    item = Listings.objects.get(title=title)
    product = Watchlist.objects.get(user=user,item=item).delete()
    wins = ListingsWon.objects.all()
    isowner = False
    won = False

    for listing in wins:
        if listing.user == request.user:
            won = True

    if item.owner == request.user:
        isowner = True

    comments = Comments.objects.all()
    commentList = []
    for comment in comments:
        if comment.item == item:
            commentList.append(comment)
    try:
        bid = Bids.objects.get(user=request.user,item=item)
        if bid.price == item.starting_bid:
            highestBidder = True
        return render(request,"auctions/item.html",{
            "title": item.title, "price": item.starting_bid, "description": item.description,
            "picture": item.picture, "category": item.category, "check": False, "owner": item.owner,
            "highestBidder": highestBidder, "isowner": isowner, "comments": commentList, "won": won
        })
    except:
        return render(request,"auctions/item.html",{
            "title": item.title, "price": item.starting_bid, "description": item.description,
            "picture": item.picture, "category": item.category, "check": False, "owner": item.owner,
            "isowner": isowner, "comments": commentList, "won": won
        })

def categories(request):
    #Links user to the webpage that displays all of the categories
    won = False
    wins = ListingsWon.objects.all()
    for listing in wins:
        if listing.user == request.user:
            won = True
    return render(request, "auctions/categories.html",{
        "categories": Categories.objects.all(), "won": won
    })

def category(request, cat):

    won = False
    wins = ListingsWon.objects.all()
    for listing in wins:
        if listing.user == request.user:
            won = True
    #Create a list for listings with a specific category
    list = []
    items = Listings.objects.all()
    #Checks between the category selcted and the listing's category
    for item in items:
        if item.category == Categories.objects.get(category=cat) and item.isOpen:
            list.append(item)
    #Path if chosen category has no listings
    if len(list) == 0:
        return render(request, "auctions/categories.html",{
            "message": f"There are no items in the {cat} category."
        })
    return render(request, "auctions/category.html", {
        "items": list, "won": won
    })

def comment(request,title):
    item = Listings.objects.get(title=title)

    if not request.POST.get('comments'):
        comments = Comments.objects.all()
        commentList = []
        for comment in comments:
            if comment.item == item:
                commentList.append(comment)

        return render(request, "auctions/item.html",{
            "title": item.title, "price": item.starting_bid,
            "description": item.description, "picture": item.picture,
            "category": item.category, "comments": commentList, "owner": item.owner,
            "message": "You have to include a review."
        })

    comment = Comments(
        user = request.user,
        item = item,
        comment = request.POST.get('comments')
    )

    comment.save()
    comments = Comments.objects.all()
    commentList = []

    for comment in comments:
        if comment.item == item:
            commentList.append(comment)

    return render(request, "auctions/item.html",{
        "title": item.title, "price": item.starting_bid,
        "description": item.description, "picture": item.picture,
        "category": item.category, "comments": commentList
    })

def bid(request,title):
    item = Listings.objects.get(title=title)
    bid = request.POST.get('bid')

    if(int(bid) <= item.starting_bid):
        message = "Your bid must be greater than the current bid."
        return render(request, "auctions/item.html",{
            "message": "Your bid must be greater than the current bid.",
            "title": item.title, "price": item.starting_bid,
            "description": item.description, "picture": item.picture,
            "category": item.category, "owner": item.owner
        })
    else:
        item.starting_bid = bid
        item.save()

        bid = Bids(
            user = User.objects.get(username=request.user),
            item = item,
            price = bid
        )
        bid.save()

        message = "Your bid was successful!"

        if item.starting_bid == bid.price:
            return render(request, "auctions/item.html",{
                "message": message, "title": item.title, "price": item.starting_bid,
                "description": item.description, "picture": item.picture,
                "category": item.category, "highestBidder": True
            })
        else:
            return render(request, "auctions/item.html",{
                "message": message, "title": item.title, "price": item.starting_bid,
                "description": item.description, "picture": item.picture,
                "category": item.category
            })

def close(request,title):
    winner = ""

    item = Listings.objects.get(title=title)
    bids = Bids.objects.all()

    for bid in bids:
        if bid.item == item and bid.price == item.starting_bid:
            winner = bid.user
            open = False

    listing = ListingsWon(
        user = winner,
        item = item
    )
    listing.save()

    item.isOpen = False
    item.save()

    return render(request, "auctions/item.html",{
    "title": item.title, "price": item.starting_bid, "description": item.description,
    "picture": item.picture, "category": item.category, "owner": item.owner, "winner":winner,
    "open": open,
    })

def listingsWon(request):
    wins = ListingsWon.objects.all()
    won = []

    for listing in wins:
        if listing.user == request.user:
            title = listing.item
            item = Listings.objects.get(title=title)
            won.append(item)

    return render(request, "auctions/listingsWon.html",{
        "items": won, "won": True,
    })

def item(request, title):
    if title == "admin":
        return HttpResponseRedirect(reverse('admin:index'))
    else:
        try:
            won = False
            check = False
            isowner = False
            highestBidder = False
            commentList = []

            item = Listings.objects.get(title=title)
            bids = Bids.objects.all()
            wlist = Watchlist.objects.all()
            comments = Comments.objects.all()
            wins = ListingsWon.objects.all()

            for listing in wins:
                if listing.user == request.user:
                    won = True

            for product in wlist:
                if product.item == item and product.user == request.user:
                    check = True

            for bid in bids:
                if bid.item == item and bid.user == request.user and bid.price == item.starting_bid:
                    highestBidder = True

            for comment in comments:
                if comment.item == item:
                    commentList.append(comment)

            if item.owner == request.user:
                isowner = True

            if item.isOpen == False and highestBidder == True:
                message = f"Congratulations {request.user}! You won the auction for {item}."
                return render(request, "auctions/item.html",{
                    "title": item.title, "price": item.starting_bid, "description": item.description,
                    "picture": item.picture, "category": item.category, "owner": item.owner, "check": check,
                    "isowner": isowner, "highestBidder": highestBidder, "comments": commentList, "winningMessage":message,
                    "open": item.isOpen, "won": won
                })
            else:
                return render(request, "auctions/item.html",{
                    "title": item.title, "price": item.starting_bid, "description": item.description,
                    "picture": item.picture, "category": item.category, "owner": item.owner, "check": check,
                    "isowner": isowner, "highestBidder": highestBidder, "comments": commentList, "open": item.isOpen,
                    "won": won
                })
        except:
            HttpResponse("Something went wrong, try again later.")
