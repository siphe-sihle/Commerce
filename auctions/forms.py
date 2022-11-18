#from tkinter import Widget
from auctions.models import *
from django.db import models
from django.forms import FloatField, ModelForm, NumberInput, Textarea
from django import forms
#from .models import *

# Create an "add listing" form
"""
Requirements:
1. Specify a title for the listing,
2. a text-based description,
3. and what the starting bid should be.
4. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
"""

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['pub_date', 'mod_date', 'bidders', 'comments', 'category']
        widget = {
            'title': Textarea(attrs= {"class": "form-control"}),
            'description': Textarea(attrs={'class': 'form-control'})
        }
    pass

# Nov 2022 implementation
class ImgForm(forms.Form):
    #name = forms.CharField()
    image_file = forms.ImageField()

