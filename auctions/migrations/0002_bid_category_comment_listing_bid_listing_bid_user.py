# Generated by Django 4.0.3 on 2022-06-09 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(default='no category listed', max_length=20, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
                ('current_bid', models.FloatField(blank=True, default=0.0)),
                ('bids', models.ManyToManyField(blank=True, related_name='bidders', to='auctions.bid')),
                ('comment', models.ManyToManyField(blank=True, related_name='Commented_by', to='auctions.comment')),
                ('listing_category', models.ManyToManyField(blank=True, related_name='category', to='auctions.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listed_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidded_listed', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]