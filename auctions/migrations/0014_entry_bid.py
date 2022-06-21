# Generated by Django 4.0.3 on 2022-06-17 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_bid_amount_bid_bidder_bid_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_bid', to='auctions.bid'),
        ),
    ]
