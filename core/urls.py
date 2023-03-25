from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('checkout', views.checkout, name='checkout'),
    path('cart', views.cart, name='cart'),
    path('category/<int:id>', views.category, name='category'),
    path('add_to_cart/<pk>', views.add_to_cart, name="add_to_cart"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
