# Generated by Django 5.1.1 on 2024-11-26 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0043_address_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address',
            new_name='current_location',
        ),
    ]