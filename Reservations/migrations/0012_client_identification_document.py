# Generated by Django 4.2 on 2023-04-20 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations', '0011_room_price_per_day_alter_reservation_pay_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='identification_document',
            field=models.CharField(default='7333', max_length=15),
        ),
    ]
