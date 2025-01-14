# Generated by Django 5.1.1 on 2024-11-05 04:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kfd', '0023_instatus_outstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instatus',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='outstatus',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='user',
        ),
        migrations.CreateModel(
            name='Supplier_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('supplier_reg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_status', to='kfd.registration')),
            ],
        ),
        migrations.DeleteModel(
            name='Custmer',
        ),
        migrations.DeleteModel(
            name='InStatus',
        ),
        migrations.DeleteModel(
            name='OutStatus',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
    ]
