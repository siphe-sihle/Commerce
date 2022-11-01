# Generated by Django 4.0.3 on 2022-06-17 14:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_bid_listing_remove_user_bids_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='price',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='mod_date',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='starting_bid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='user',
        ),
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('mod_date', models.DateField(default=datetime.date.today)),
                ('bidders', models.ManyToManyField(blank=True, related_name='buyers', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='on_sale', to='auctions.listing')),
            ],
        ),
    ]
