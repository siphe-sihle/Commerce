# Generated by Django 4.0.3 on 2022-06-28 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_comment_commented_by_comment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(null=True, related_name='listing_comments', to='auctions.comment'),
        ),
    ]
