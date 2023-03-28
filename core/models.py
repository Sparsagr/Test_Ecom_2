from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


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

    def product_count(self):
        return self.product_set.count()


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

class Reviews(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    review = models.CharField(max_length=5000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")

    def __str__(self) -> str:
        return self.name

class Offer(models.Model):
    image = models.ImageField(upload_to="offers/")


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(
        max_length=100, unique=True, default=None, blank=True, null=True)
    datetime_ofpayment = models.DateTimeField(auto_now_add=True)
    order_delivered = models.BooleanField(default=False)
    order_recieved = models.BooleanField(default=False)

    razorpay_order_id = models.CharField(
        max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(
        max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(
        max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id = self.datetime_ofpayment.strftime(
                'PAY2ME%Y%m%dODR') + str(self.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_count(self):
        order = Order.objects.get(pk=self.pk)
        return order.items.count()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.message

class Newsletter(models.Model):
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email