# Generated by Django 5.1.3 on 2024-11-30 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_reservationmodel_is_cancelled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationmodel',
            name='is_cancelled',
        ),
    ]
