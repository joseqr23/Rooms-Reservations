# Generated by Django 4.2 on 2023-04-19 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations', '0007_rename_client_id_reservation_client_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='client',
            new_name='client_id',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='room',
            new_name='room_id',
        ),
    ]