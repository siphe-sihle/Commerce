from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:id>", views.listing_view, name="listings"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("category", views.category_view, name="category"),
    path("categories/<int:category_id>", views.filtered_category_view, name="filtered"),
    path("error", views.error_view, name="error"),
    path("mylistings", views.my_listings, name="mylistings")
]
