from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from core.forms import *
from core.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    offer = Offer.objects.get(id=1)

    parameters = {
        'products': products,
        'categories': categories,
        'offer': offer
    }

    return render(request, 'core/index.html', parameters)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print('True')
            form.save()
            print("Data Saved Succesfully")
            messages.success(request, "product added successfully")
            return redirect('add_product')
        else:
            print("Not Working")
            messages.info("Product is not added , Try again")
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})


def checkout(request):
    return render(request, 'core/checkout.html')


@login_required
def cart(request):
    if Cart.objects.filter(user=request.user).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        cart_itmes = Cart.objects.filter(user=request.user)
        len_of_cart = len(Cart.objects.all())
        return render(request, 'core/cart.html', {'order': order, 'len_of_cart': len_of_cart, 'cart_itmes': cart_itmes})
    return render(request, 'core/cart.html', {'message': "Your cart is empty"})


def add_to_cart(request, pk):
    # Get that perticular product of id = pk

    product = Product.objects.get(pk=pk)

    # create order item
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )


# get query set of order object of particular user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added Quantity Item")

        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order.item)

        product = get_object_or_404(pk, product__pk=pk)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


def category(request, id):
    category = Category.objects.get(id=id)

    products = Product.objects.filter(category=category)

    parameters = {
        "category": category,
        "products": products
    }

    return render(request, "core/category.html", parameters)
