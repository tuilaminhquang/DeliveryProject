# Generated by Django 4.0.3 on 2022-03-29 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryApp', '0004_delete_shipper'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_shipper',
            field=models.BooleanField(default=False),
        ),
    ]
