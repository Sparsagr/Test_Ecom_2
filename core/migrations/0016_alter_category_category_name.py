# Generated by Django 4.1.7 on 2023-05-28 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=1000),
        ),
    ]
