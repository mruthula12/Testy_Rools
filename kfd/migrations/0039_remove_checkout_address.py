# Generated by Django 5.1.1 on 2024-11-18 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0038_alter_checkout_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='address',
        ),
    ]
