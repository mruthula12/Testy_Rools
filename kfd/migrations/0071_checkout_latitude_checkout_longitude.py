# Generated by Django 5.1.1 on 2024-12-18 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0070_remove_checkout_latitude_remove_checkout_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
