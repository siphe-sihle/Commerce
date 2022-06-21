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
    creator = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user", null=True)

    def __str__(self):
        return f"{self.title} - Creator: {self.creator}"
    #starting_bid = models.FloatField(default= 0.00, null= False, blank = True)
 
class Bid(models.Model):
    amount = models.FloatField(null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="on_auction", null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True)

    def __str__(self):
        return f"({self.id}) {self.amount} bidder: {self.bidder}"

 # Listing Entry - model for storing listing entries
class Entry(models.Model):
    # Create a Listing field, reference to the Listing Table
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="on_sale")
    bid = models.ForeignKey(Bid, on_delete= models.CASCADE, related_name="current_bid", null=True)
    bidders = models.ManyToManyField(User, blank=True, related_name="buyers")
    pub_date = models.DateField(default=date.today)
    mod_date = models.DateField(default=date.today)

    def __str__(self):
        return f"({self.id}) {self.listing}"


class Comment(models.Model):
    pass