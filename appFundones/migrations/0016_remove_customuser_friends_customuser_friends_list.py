# Generated by Django 5.0.7 on 2024-09-27 06:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFundones', '0015_friendrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='friends',
        ),
        migrations.AddField(
            model_name='customuser',
            name='friends_list',
            field=models.ManyToManyField(blank=True, related_name='friends_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
