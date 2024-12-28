# Generated by Django 5.1.1 on 2024-11-18 04:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0035_remove_checkout_chekout_reg_remove_checkout_product_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_number', models.CharField(blank=True, max_length=10, null=True)),
                ('apartment', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('added_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_preparing', models.BooleanField(default=False)),
                ('is_prepared', models.BooleanField(default=False)),
                ('is_delivery_partner_arrived', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('chekout_reg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kfd.registration')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kfd.product')),
            ],
        ),
    ]
