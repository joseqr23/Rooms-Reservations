# Generated by Django 4.2 on 2023-04-20 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations', '0015_alter_reservation_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='stay_days',
            field=models.IntegerField(),
        ),
    ]
