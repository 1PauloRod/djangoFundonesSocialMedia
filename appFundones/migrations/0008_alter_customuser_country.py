# Generated by Django 5.0.7 on 2024-08-01 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appFundones', '0007_alter_customuser_bday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
