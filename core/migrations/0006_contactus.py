# Generated by Django 4.1.7 on 2023-03-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=5000)),
            ],
        ),
    ]
