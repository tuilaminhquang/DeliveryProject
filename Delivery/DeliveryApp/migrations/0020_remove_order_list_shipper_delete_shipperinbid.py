# Generated by Django 4.0.3 on 2022-04-28 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryApp', '0019_alter_shipperinbid_shipper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='list_shipper',
        ),
        migrations.DeleteModel(
            name='ShipperInBid',
        ),
    ]
