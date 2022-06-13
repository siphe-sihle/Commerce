# Generated by Django 4.0.3 on 2022-06-13 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_listing_category_delete_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='current_bid',
            new_name='starting_bid',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='comment',
        ),
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='listing_bids', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
