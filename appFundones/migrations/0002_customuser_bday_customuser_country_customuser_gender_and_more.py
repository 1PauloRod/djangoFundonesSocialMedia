# Generated by Django 5.0.7 on 2024-07-31 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFundones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bday',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
