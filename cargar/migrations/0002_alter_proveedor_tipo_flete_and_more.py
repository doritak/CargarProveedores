# Generated by Django 5.1.7 on 2025-04-07 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='tipo_flete',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cargar.tipoflete'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='transporte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cargar.transporte'),
        ),
    ]
