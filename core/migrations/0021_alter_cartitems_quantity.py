# Generated by Django 4.1.7 on 2023-06-17 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_remove_cart_product_cartitems"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitems",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
