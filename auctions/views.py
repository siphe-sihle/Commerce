from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from auctions.forms import *

def index(request):
    # Get all listings from the database
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})

# Listing view
def listing_view(request, id):
    
    # if request method is "POST" i.e if logged in user places a bid on a listing
    if request.method == "POST":
        if 'place' in request.POST:

            # let the user post/place a bid on a listing item
            # Get user id of logged in user
            get_creator = int(request.POST["creator"])

            # Create user Object
            user_obj = User.objects.get(pk=get_creator)

            # Get placed bid on listing:
            get_bid = float(request.POST["bid"])

            # get current listing:
            current_listing = Listing.objects.get(pk=id)

            # Insert this bid for the current listing into the Bid Table
            Bid.objects.create(amount=get_bid, listing=current_listing, bidder=user_obj)
            messages.info(request, "Bid probably placed!")

            # Render the current listing page after placing a bid
            #return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
            
        if 'wishlist' in request.POST:
            current_listing = Listing.objects.get(pk=id)
            # Note: The line below does not work when using "request.user" because that is an object, not a number or string 
            curr_user = int(request.POST["creator"])
            print(f"current: {curr_user}")
            userobj = User.objects.get(pk=curr_user)
            #add item to user's watchlist, 1st check if listing is already in watchlist: FIX LATER - WORKS!
            user_watchlist = Watchlist.objects.filter(user=curr_user)
            for item in user_watchlist:
                if item.listing.id == current_listing.id:
                    messages.info(request, 'listing ALREADY Added to wishlist!')
                    return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
            
            Watchlist.objects.create(listing=current_listing, user=userobj)
            messages.info(request, 'listing Added to wishlist!')

        return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
    # Else if request method is "GET", just render the current listing page:
    
    # Get particular listing details using the listing id
    listing = Listing.objects.get(pk = id)
    # Get all comments for a particular listing using filter()
    comments = Comment.objects.filter(listing_id = id)

    # Get Current listing's bid, NEEDS SOME TWEAKING WHEN NEW VALUE IS ADDED AS THE CURRENT BID
    #Fixed - Orderd in descending order, the first one in order is the current bid
    current_bid = listing.offers.order_by("-amount").first()
    #current_bid = Bid.objects.filter(listing_id = id).last()

    # Now get the list of all categories for a particular listing
    categories = Category.objects.all()
    # Categories for a specific listing
    listing_categories = listing.category.all()

    # Number of bids for the current listing:
    bid_count = listing.offers.count()

    return render(request, "auctions/listing.html", {"listing": listing, "comments": comments, "current_bid": current_bid,
    "categories": listing_categories,
    "count_offers": bid_count})
    pass

# New Listing view
def create_listing(request):

    if request.method == "POST":
        # User in question (logged in user) that is creating the listing, get ID of the user, data lives in request.POST
        get_creator = int(request.POST["creator"])
        print(get_creator)
        get_title = request.POST["title"]
        print(f"title: {get_title}")
        get_description = request.POST["description"]
        print(f"description: {get_description}")

        get_bid = float(request.POST["bid"])
        print(f"bid: {get_bid}")

        # Here's how its gonna work:
        # 1. Create and save a listing 1st before saving the amount for the listing.
        # 2. That listing amount is the initial bid for the listing

        # 1
        creator_obj = User.objects.get(pk = get_creator)
        create_listing = Listing.objects.create(title = get_title, description = get_description, creator = creator_obj)

        # 2 Now add bid obj to be able to add amount to a particular listing
        listing_id = create_listing.id

        # Create bid for this particular listing
        bid_obj = Bid.objects.create(amount = get_bid, listing = create_listing, bidder = creator_obj) 

        #2.1 update the Listing field for the bid

        # Redirect user to the newly added listing page
        return HttpResponseRedirect(reverse("listings", args={f"{listing_id}"}))

    # else if request method is "GET", just render the form
    
    # User in question that is creating the listing, get ID of the user, data lives in request.POST
    f = CreateListingForm(request.POST)

    #For now we will create the form manually for the simplicity of it
    # Get all the models and then create the listing

    return render(request, "auctions/create.html", {"form": f})

# Watchlist view
#@login_required
def watchlist_view(request):
    # Get current user like so:
    current_user = request.user
    print(f"current user: {current_user.id}")
    return render(request, "auctions/watchlist.html", {"items": Watchlist.objects.filter(user_id=current_user)})
    pass


# Categories view
def category_view(request):
    pass


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
