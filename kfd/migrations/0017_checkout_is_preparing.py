# Generated by Django 5.1.1 on 2024-11-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0016_checkout_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='is_preparing',
            field=models.BooleanField(default=False),
        ),
    ]
