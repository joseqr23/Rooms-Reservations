# Generated by Django 4.2 on 2023-04-19 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations', '0006_rename_client_reservation_client_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='client_id',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='room_id',
            new_name='room',
        ),
    ]
