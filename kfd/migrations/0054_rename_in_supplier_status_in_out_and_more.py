# Generated by Django 5.1.1 on 2024-11-30 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0053_rename_in_out_supplier_status_in_supplier_status_out'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier_status',
            old_name='In',
            new_name='in_out',
        ),
        migrations.RemoveField(
            model_name='supplier_status',
            name='Out',
        ),
    ]