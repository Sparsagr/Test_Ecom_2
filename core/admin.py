from django.contrib import admin
from core.models import *
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ("last_login", "is_superuser", "is_staff", "is_active",
               "date_joined", "groups", "user_permissions", "password")


admin.site.register((Category, Order, OrderItem, Cart,
                    ContactUs, Reviews, checkout, Profile))


class ReviewInline(admin.StackedInline):
    model = Reviews


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]

admin.site.register(MyOrders)