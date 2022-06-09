from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length= 30)
    description = models.CharField(max_length= 200)
    current_bid = models.FloatField(default= 0.00, null= False, blank = True)
    #Define User object that posted the listing
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "listed_by")
    #define a many to many relationship to bids
    bids = models.ManyToManyField("Bid", blank= True, related_name= "bidders")

    #Define many to many relationship to both comments and categories
    comment = models.ManyToManyField("Comment", blank= True, related_name= "Commented_by")
    listing_category = models.ManyToManyField("Category", blank= True, related_name= "category")

    def __str__(self):
        return f"id: {self.id}, Title: {self.title}, Description:{self.description}, category: {self.listing_category}."

class Bid(models.Model):
    price = models.FloatField(default= 0.00, null= False)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "bidder")
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name= "bidded_listed")

    def __str__(self):
        return f"id: {self.id} user: {self.user} Listing: {self.listing}"

class Comment(models.Model):
    description = models.CharField(max_length= 200)
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "commenter")

    def __str__(self):
        return f"Description: {self.description}, user: {self.user}."

class Category(models.Model):
    name = models.CharField(max_length= 20, primary_key= True, unique= True, default= "no category listed")

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"