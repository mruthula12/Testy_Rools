# Generated by Django 5.1.1 on 2024-10-31 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0013_remove_checkout_user_checkout_chekout_reg_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='email',
        ),
        migrations.AlterField(
            model_name='checkout',
            name='chekout_reg',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='kfd.registration'),
        ),
    ]