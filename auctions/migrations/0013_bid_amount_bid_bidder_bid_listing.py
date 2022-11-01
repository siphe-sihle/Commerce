# Generated by Django 4.0.3 on 2022-06-17 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_remove_bid_price_remove_bid_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_auction', to='auctions.listing'),
        ),
    ]
