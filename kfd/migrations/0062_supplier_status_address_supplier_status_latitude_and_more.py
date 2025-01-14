# Generated by Django 5.1.1 on 2024-12-06 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0061_remove_checkout_delivered_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_status',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='supplier_status',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='supplier_status',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
