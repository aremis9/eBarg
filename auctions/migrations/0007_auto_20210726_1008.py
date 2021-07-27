# Generated by Django 3.2.5 on 2021-07-26 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commentor',
        ),
        migrations.AddField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to='auctions.user'),
            preserve_default=False,
        ),
    ]