# Generated by Django 4.0.3 on 2022-06-14 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.BigIntegerField(null=True),
        ),
    ]
