# Generated by Django 4.0.3 on 2022-06-29 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_alter_listing_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='none', max_length=20),
        ),
    ]
