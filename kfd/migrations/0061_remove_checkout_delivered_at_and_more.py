# Generated by Django 5.1.1 on 2024-12-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0060_remove_checkout_is_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='delivered_at',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='checkout',
            name='status',
        ),
        migrations.RemoveField(
            model_name='supplier_status',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='supplier_status',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='supplier_status',
            name='location_name',
        ),
        migrations.RemoveField(
            model_name='supplier_status',
            name='longitude',
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_delivered_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_delivery_partner_arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_out_of_delivery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_prepared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checkout',
            name='is_preparing',
            field=models.BooleanField(default=False),
        ),
    ]