from django.urls import path
from . import views

try:
    urlpatterns = [
        path('', views.index, name='index'),
        path('shop', views.shop, name='shop'),
        path('checkout', views.checkout, name='checkout'),
        path('cart', views.cart, name='cart'),
        path('contactus', views.contactus, name='contactus'),
        path('invoice/<order_id>/',views.generate_invoice, name='generate_invoice'),
        path('managecontactus', views.managecontactus, name='managecontactus'),
        path('saveReview/<slug>', views.saveReview, name="saveReview"),
        path('search', views.search, name="search"),
        path("payment-successfull/handlerequest/", views.handlerequest, name="handlerequest"),
        path('<slug>', views.products, name='products'),
        path('managenewsletter', views.managenewsletter, name='managenewsletter'),
        path('category/<int:id>', views.category, name='category'),
        path('add_to_cart/<pk>', views.add_to_cart, name="add_to_cart"),
        path('remove_cart_items/<pk>', views.remove_cart_items,
            name="remove_cart_items"),
    ]
except Exception as e:
    print(e)
