# Generated by Django 5.0.7 on 2024-09-27 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appFundones', '0016_remove_customuser_friends_customuser_friends_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='friends_list',
            new_name='friends',
        ),
    ]
