# Generated by Django 4.0.3 on 2022-06-14 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_bid_listings_remove_listing_bids_bid_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='user_bids', to='auctions.bid'),
        ),
        migrations.AddField(
            model_name='user',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='user_listings', to='auctions.listing'),
        ),
    ]
