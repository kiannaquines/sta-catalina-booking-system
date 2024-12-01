# Generated by Django 5.0.7 on 2024-11-25 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationmodel',
            name='location',
            field=models.CharField(help_text='Your location to deliver', max_length=255),
        ),
        migrations.AlterField(
            model_name='reservationmodel',
            name='reserved_by',
            field=models.ForeignKey(limit_choices_to={'user_type': 'Regular User'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='truckmodel',
            name='driver',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'Driver'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
