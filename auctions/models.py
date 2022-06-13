from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    price = models.FloatField(default= 0.00, null= False)
    # User that placed the bid, and their subsequent bids
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "bids", blank=True)

    def __str__(self):
        return f"id: {self.id} user: {self.user}"


class Listing(models.Model):
    title = models.CharField(max_length= 30)
    description = models.CharField(max_length= 200)
    starting_bid = models.FloatField(default= 0.00, null= False, blank = True)
    #Define User that posted the listing. This is the user field for the model
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "listings")
    bids = models.ManyToManyField(Bid, blank = True, related_name= "listing_bids")
    # Define the many bids that could be placed on a particular listing 

    def __str__(self):
        return f"id: {self.id} Title: {self.title}, Description:{self.description} Current Bid: {self.starting_bid}, user_id: {self.user}"


class Comment(models.Model):
    pass