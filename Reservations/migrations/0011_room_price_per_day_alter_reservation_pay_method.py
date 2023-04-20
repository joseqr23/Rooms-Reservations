# Generated by Django 4.2 on 2023-04-20 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations', '0010_alter_reservation_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price_per_day',
            field=models.FloatField(default=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pay_method',
            field=models.CharField(choices=[('credit_card', 'CREDIT_CARD'), ('debit_card', 'DEBIT_CARD'), ('cash', 'CASH'), ('other', 'OTHER')], max_length=11),
        ),
    ]
