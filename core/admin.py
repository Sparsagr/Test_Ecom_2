from django.contrib import admin
from core.models import *
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ("last_login", "is_superuser", "is_staff", "is_active",
               "date_joined", "groups", "user_permissions", "password")


admin.site.register((Category, Order, OrderItem, 
                    ContactUs, Reviews, checkout, Profile))

class CartItemsInline(admin.StackedInline):
    model = CartItems

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemsInline]


class ReviewInline(admin.StackedInline):
    model = Reviews

class ProductImageInline(admin.StackedInline):
    model=ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ProductImageInline]




class MyOrderItemInline(admin.StackedInline):
    model=MyOrderItem

@admin.register(MyOrders)
class MyOrderAdmin(admin.ModelAdmin):
    inlines = [MyOrderItemInline]