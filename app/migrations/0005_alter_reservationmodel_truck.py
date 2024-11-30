# Generated by Django 5.1.3 on 2024-11-30 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_reservationmodel_date_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationmodel',
            name='truck',
            field=models.ForeignKey(blank=True, help_text='Truck to deliver', limit_choices_to={'driver__user_type': 'Driver'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.truckmodel'),
        ),
    ]
