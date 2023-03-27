from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from core.forms import *
from core.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


def index(request):
    products = Product.objects.all()
    new_prods = products[::-1]
    f_new_prods = new_prods[0]
    new_prods = new_prods[1:3]
    categories = Category.objects.all()
    offer = Offer.objects.get(id=1)
    if(request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        parameters = {
            'products': products,
            'categories': categories,
            'offer': offer,
            'len_of_cart':len_of_cart,
            'new_prods':new_prods,
            'f_items':f_new_prods
        }
        return render(request, 'core/index.html', parameters)
    parameters = {
        'products': products,
        'categories': categories,
        'offer': offer,
        'new_prods':new_prods,
        'f_items':f_new_prods
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
    if(request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        print(len_of_cart)
        return render(request, 'core/checkout.html',{'len_of_cart':len_of_cart})
    else:
        return render(request, 'core/checkout.html')



def cart(request):
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user).exists():
            order = Order.objects.get(user=request.user, ordered=False)
            cart_itmes = Cart.objects.filter(user=request.user)
            len_of_cart = len(Cart.objects.filter(user=request.user))
            return render(request, 'core/cart.html', {'order': order, 'len_of_cart': len_of_cart, 'cart_itmes': cart_itmes})
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request, 'core/cart.html', {'message': "Your cart is empty",'len_of_cart': len_of_cart})
    return redirect("/accounts/user_login")

def add_to_cart(request, pk):
    if request.user.is_authenticated:
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
    return redirect("/accounts/user_login")


def category(request, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)

    parameters = {
        "category": category,
        "products": products
    }

    return render(request, "core/category.html", parameters)

def products(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        if(request.user.is_authenticated):
            len_of_cart = len(Cart.objects.filter(user=request.user))
            return render(request,"core/product-details.html", {'len_of_cart':len_of_cart, 'prodDescp':product})
        return render(request,"core/product-details.html", {'prodDescp':product})

    except Exception as e:
        return HttpResponse("404 Not Found")
    

def shop(request):
    products= Product.objects.all()
    if(request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request,"core/shop.html",{'len_of_cart':len_of_cart,'products':products})
    return render(request,"core/shop.html",{'products':products})

def contactus(request):
    if(request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request,"core/contact-us.html",{'len_of_cart':len_of_cart})
    return render(request,"core/contact-us.html")

def remove_cart_items(request,pk):
    cart_product = Cart.objects.filter(pk=pk)
    cart_product.delete()
    return redirect('cart')

def managecontactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        print(name,email,subject,message)
        contact_details =  ContactUs(name=name, email=email, subject=subject, message=message)
        contact_details.save()
        return redirect("/contactus")
    return render(request, "core/404.html")

def managenewsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        newsletter = Newsletter(email=email)
        newsletter.save()
        return redirect("/")
    return render(request, "core/404.html")