from distutils.log import error
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from auctions.forms import *
from django.db.models import Avg, Max, Min, Sum

def index(request):
    # Get all listings from the database
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})

# Listing view
def listing_view(request, id):

    # if request method is "POST" i.e if logged in user places a bid on a listing
    if request.method == "POST":
        # Global variables under the "POST" condition that are consistent and obey scope throughout this "listing_view":
        get_creator = int(request.POST["creator"])
        user_obj = User.objects.get(pk=get_creator)
        current_listing = Listing.objects.get(pk=id)
        if 'place' in request.POST:

            # let the user post/place a bid on a listing item
            # Get user id of logged in user: works
            #get_creator = int(request.POST["creator"])

            # Create user Object: works
            #user_obj = User.objects.get(pk=get_creator)

            # Get placed bid on listing: works
            get_bid = float(request.POST["bid"])
            
            #Error checking: Check if the bid is at least as large as the starting bid, and must be greater than any other bids that have been placed (if any)

            # Get Max bid for the listing
            max_bid = current_listing.offers.all().aggregate(Max('amount'))
            
            if max_bid.get('amount__max') > get_bid:
                return render(request, "auctions/error.html",{"message": f"R{get_bid} amount is lower than the current bid! Place a bid that is greater than that of the current bid!"})
            
            # Else continue placing the bid
            
            # Insert this bid for the current listing into the Bid Table
            Bid.objects.create(amount=get_bid, listing=current_listing, bidder=user_obj)
            messages.info(request, "Bid probably placed!")

            # Render the current listing page after placing a bid
            #return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
        
        # Global variables for our choice of submit buttons below
        user_watchlist = Watchlist.objects.filter(user=get_creator)

        if 'add' in request.POST:
            #current_listing = Listing.objects.get(pk=id)
            # Note: The line below does not work when using "request.user" because that is an object, not a number or string 
            #get_creator = int(request.POST["creator"])
            print(f"current: {get_creator}")
            #userobj = User.objects.get(pk=get_creator)
            #add item to user's watchlist, 1st check if listing is already in watchlist: FIX LATER - WORKS!
            
            for item in user_watchlist:
                if item.listing.id == current_listing.id:
                    messages.info(request, 'listing ALREADY Added to wishlist!')
                    #Just check the status field for the particular listing to true for now
                    item.status = True
                    #update the item's status
                    item.save(update_fields=['status'])
                    return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
            
            Watchlist.objects.create(listing=current_listing, user=user_obj, status=True)
            messages.info(request, f'{current_listing.title} Added to wishlist!')
        
        if 'remove' in request.POST:
            for item in user_watchlist:
                if item.listing.id == current_listing.id:
                    # Remove that particular listing from user's Watchlist
                    item.status = False
                    item.save()
                    item.delete()
                    messages.info(request, f'{current_listing.title} REMOVED From wishlist!')
                    return HttpResponseRedirect(reverse("listings", args={f"{id}"}))
        
        # Add signed-in user's ability to close the listing
        if "close" in request.POST:
            # Check if current listing has been created by signed-in user
            user_listings = Listing.objects.filter(creator=user_obj)

            # Insert the auction winner for the listing  into the db
            max_amount = current_listing.offers.aggregate(Max('amount'))
            current_bid = max_amount.get('amount__max')
            
            # firstly filter out the winning bid from the current listing
            winning_bid = current_listing.offers.filter(amount=current_bid)
            # Extract winning bid from the select query above
            buyer_obj = winning_bid[0].bidder

            auction_winner = buyer_obj.username

            if current_listing in user_listings:
                #Give logged in user the ability to close the auction and update listing's "active" field to False
                current_listing.active = False
                # Now perform winner "INSERT" AND update the db
                current_listing.winner = buyer_obj
                current_listing.save(update_fields=['active', 'winner'])

            messages.info(request, f'{current_listing.title}: Auction has now been closed!')    
            pass

        # Add signed-in user's ability to post comments to the listing
        if "comment" in request.POST:
            # get listing's object, current_user objects and then create the comment in the db
            
            #Get comment description
            get_description = request.POST[f"add_comments"]
            logged_in_user = request.user
            Comment.objects.create(description=get_description, commented_by=logged_in_user, listing=current_listing)
            pass
        
        # What if our "add to wishlist" button/text changes dynamically depending on whether the listing is added to wishlist or not? Lets see below
        # We'll figure that out as we go

        return HttpResponseRedirect(reverse("listings", args={f"{id}"}))


    # Else if request method is "GET", just render the current listing page:
    
    # Get particular listing details using the listing id
    listing = Listing.objects.get(pk = id)
    # Get all comments for a particular listing using filter()
    comments = Comment.objects.filter(listing_id = id)

    # Get Current listing's bid, NEEDS SOME TWEAKING WHEN NEW VALUE IS ADDED AS THE CURRENT BID
    #Fixed - Orderd in descending order, the first one in order is the current bid
    max_amount = listing.offers.aggregate(Max('amount'))
    min_amount = listing.offers.aggregate(Min('amount'))
    starting_bid = min_amount.get('amount__min')
    current_bid = max_amount.get('amount__max')
    print(f"current_amount: {current_bid}")
    #current_bid = Bid.objects.filter(listing_id = id).last()

    # Now get the list of all categories for a particular listing
    categories = Category.objects.all()
    # Categories for a specific listing
    listing_categories = listing.category.all()

    # Number of bids for the current listing:
    bid_count = listing.offers.count()

    # Actual number of bids excluding the minimum bid placed by the listing creator
    actual_bid_count = bid_count - 1
    
    if actual_bid_count < 0:
        actual_bid_count = 0

    # Checking whether item is in logged-in user's watchlist
    curr_user = request.user
    watchlist_status = Watchlist.objects.filter(user=curr_user.id)

    # Initialise wishlist_status
    status = None
    print(f"watchlist: {watchlist_status}")

    # Check if current listing in listing page is in the watchlist for the currently logged_in user
    for item in watchlist_status:
        if item.listing.id == listing.id:
            status = True

    # CLOSING THE AUCTION: Check if the logged-in user is the one who created the listing, to be able to display/hide the "close auction" button
    
    # Listing activity status
    listing_activity = listing.active

    if curr_user.id == listing.creator.id and listing_activity == True:
        close_auction_btn = True
    else:
        close_auction_btn = False

    # Check if logged-in user is the one who won the auction i.e signed in on a closed listing page. 
    #TODO
    
    # firstly filter out the winning bid from the current listing

    winning_bid = listing.offers.filter(amount=current_bid)
    # Extract winning bid obj
    buyer_obj = listing.winner

    # Now check if the logged in user is the winner of the auction
    # UPDATE: already did that on the template
    
    # Only render the listing page if the listing is active: We canmake that check on the template itself
    return render(request, "auctions/listing.html", {"listing": listing, "comments": comments, "current_bid": current_bid,
    "minimum_bid": starting_bid,
    "categories": listing_categories,
    "count_offers": actual_bid_count,
    "status": status,
    "listing_activity": listing_activity,
    "close_auction_btn": close_auction_btn,
    "buyer_obj": buyer_obj})
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

        # Get (a list) of categories a user will select when creating a listing
        get_categories = request.POST.getlist("categories")
        print(f"selected categories: {get_categories}")

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

    return render(request, "auctions/create.html", {"categories": Category.objects.all().order_by('name').values()})

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
    # get all categories from the database

    return render(request,"auctions/category.html",{"categories": Category.objects.all().order_by('name').values()})
    pass

# Filtered catgories view

def filtered_category_view(request, category_id):
    # get all listings that belong to a particular category

    category_name = Category.objects.get(pk=category_id)

    # Listings that belong to a certain category_id, using the category_name object

    Category_listings = Listing.objects.filter(category=category_name)

    return render(request, "auctions/filtered.html", {"listings": Category_listings,
    "category": category_name})

# Error view

def error_view(request):

    return render(request, "auctions/error.html", {"message": "What did you do?!"})

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
