# Generated by Django 5.1.1 on 2024-10-30 12:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0011_remove_checkout_added_date_checkout_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]