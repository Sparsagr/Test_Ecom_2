from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .emails import send_Account_Activation_mail
import uuid

# Create your models here.


class Customer(User):
    phone_field = models.CharField(max_length=12, blank=False)
    address_field = models.CharField(max_length=255)
    pin_code = models.IntegerField(null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=1000)

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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images")

    def __str__(self) -> str:
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def set_quantity(self, quantity):
        self.quantity = quantity

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
    isPaid = models.BooleanField(default=False)
    orderID = models.CharField(max_length=150, blank=True , null=True)
    firstname = models.CharField(max_length=25, blank=True, null=True)
    lastname = models.CharField(max_length=25, blank=True, null=True)
    Address = models.CharField(max_length=1000, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.message

class checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_adress = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    forgot_password_token = models.CharField(
        max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    is_cv_uploaded = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username + " - " + (lambda: "Not Verified", lambda: "Verified User")[self.is_email_verified]()


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_Account_Activation_mail(email, email_token)
    except Exception as e:
        print(e)

class MyOrders(models.Model):
    user = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name= "order")
    order = models.ForeignKey(Cart , on_delete=models.CASCADE, related_name= "Cart")


