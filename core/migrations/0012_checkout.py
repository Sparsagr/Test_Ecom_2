# Generated by Django 4.1.5 on 2023-04-21 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0011_reviews"),
    ]

    operations = [
        migrations.CreateModel(
            name="checkout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street_adress", models.CharField(max_length=100)),
                ("apartment_address", models.CharField(max_length=100)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("zip_code", models.CharField(max_length=15)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
