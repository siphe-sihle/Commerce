# Generated by Django 4.0.3 on 2022-08-02 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]