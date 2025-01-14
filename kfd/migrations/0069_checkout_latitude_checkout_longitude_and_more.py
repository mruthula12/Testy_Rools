# Generated by Django 5.1.1 on 2024-12-13 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0068_address_latitude'),
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
        migrations.AddField(
            model_name='checkout',
            name='place_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
