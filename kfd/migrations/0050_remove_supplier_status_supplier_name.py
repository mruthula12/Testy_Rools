# Generated by Django 5.1.1 on 2024-11-30 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0049_alter_supplier_status_supplier_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier_status',
            name='supplier_name',
        ),
    ]
