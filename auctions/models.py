from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class User(AbstractUser):
    mobile = models.BigIntegerField(null = True)
    listings = models.ManyToManyField("Listing", blank=True, related_name="user_listings")
    bids = models.ManyToManyField("Bid", blank=True, related_name="user_bids")

class Listing(models.Model):
    title = models.CharField(max_length= 30)
    description = models.CharField(max_length= 200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    #New Addition: starting Bid
    #starting_bid = models.FloatField(null=True)
    bid = models.ManyToManyField("Bid", related_name="current_bid", null=True)
    bidders = models.ManyToManyField(User, blank=True, related_name="buyers")
    pub_date = models.DateField(default=date.today)
    mod_date = models.DateField(default=date.today)
    comments = models.ManyToManyField("Comment", related_name="listing_comments", null=True, blank=True)
    category = models.ManyToManyField("Category", related_name="listing_category", null=True)
    # New Addtion: listing activity status
    active = models.BooleanField(default=True)
    # New addition: user who won the auction
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold", null=True)

    def __str__(self):
        return f"{self.title} - Creator: {self.creator}"
    #starting_bid = models.FloatField(default= 0.00, null= False, blank = True)
 
class Bid(models.Model):
    amount = models.FloatField(default = 0.0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="offers", null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True)

    def __str__(self):
        return f"({self.id}) {self.amount} bidder: {self.bidder} Listing: {self.listing}"

 # Listing Entry - model for storing listing entries

class Entry(models.Model):
    # Create a Listing field, reference to the Listing Table
    """
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="on_sale")
    bid = models.ForeignKey(Bid, on_delete= models.CASCADE, related_name="current_bid", null=True)
    bidders = models.ManyToManyField(User, blank=True, related_name="buyers")
    pub_date = models.DateField(default=date.today)
    mod_date = models.DateField(default=date.today)

    def __str__(self):
        return f"({self.id}) {self.listing}"
    """
    pass

class Comment(models.Model):
    # Create Comment description field
    description = models.CharField(max_length= 255, blank=True)
    commented_by = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "commentator", null= True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="opinions", null=True)

    def __str__(self):
        return f"{self.commented_by}, {self.description}, {self.listing}"
    
class Category(models.Model):
    # model contains an id and name fields
    name = models.CharField(max_length= 20, default="none")
    
    def __str__(self):
        return f"({self.id} {self.name})"

# Create watchlist model
class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishes")
    # status of either a listing is added to a particular user's watchlist or not. new additionto the table
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user}({self.listing})"