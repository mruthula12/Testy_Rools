# Generated by Django 5.1.1 on 2024-11-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0024_remove_instatus_supplier_remove_outstatus_supplier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier_status',
            name='in_out',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='supplier_status',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
