# Generated by Django 3.2.5 on 2021-07-26 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Vehicles', 'Vehicles'), ('Fashion', 'Fashion'), ('Books', 'Books'), ('Electronics', 'Electronics'), ('Collectibles & Art', 'Collectibles & Art'), ('Home Appliances', 'Home Appliances'), ('Toys & Hobbies', 'Toys & Hobbies'), ('Health and Beauty', 'Health and Beauty'), ('Uncategorized', 'Uncategorized')], max_length=18),
        ),
    ]
