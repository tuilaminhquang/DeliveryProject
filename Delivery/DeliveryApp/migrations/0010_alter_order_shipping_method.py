# Generated by Django 4.0.3 on 2022-03-30 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DeliveryApp', '0009_order_shippingmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', related_query_name='my_order', to='DeliveryApp.shippingmethod'),
        ),
    ]