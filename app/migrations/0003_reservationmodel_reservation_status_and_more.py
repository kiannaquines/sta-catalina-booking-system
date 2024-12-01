# Generated by Django 5.0.7 on 2024-11-26 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_reservationmodel_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationmodel',
            name='reservation_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='reservationmodel',
            name='quantity',
            field=models.IntegerField(help_text='Product quantity (Kilo or No. Sack)'),
        ),
        migrations.AlterField(
            model_name='reservationmodel',
            name='reserved_by',
            field=models.ForeignKey(help_text='Select a user who reserved', limit_choices_to={'user_type': 'Regular User'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
