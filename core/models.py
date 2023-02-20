from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(User):
    phone_field = models.CharField(max_length=12, blank=False)
    address_field = models.CharField(max_length=255)
    pin_code = models.IntegerField(null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/')

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "pk": self.pk
        })


def __str__(self):
    return self.name
