from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from core.forms import *
from core.models import *
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

import razorpay


razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))
# Create your views here.


def index(request):
    products = Product.objects.all()
    new_prods = products[::-1]
    f_new_prods = new_prods[0]
    new_prods = new_prods[1:3]
    categories = Category.objects.all()
    
    if (request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        parameters = {
            'products': products,
            'categories': categories,
            
            'len_of_cart': len_of_cart,
            'new_prods': new_prods,
            'f_items': f_new_prods
        }
        return render(request, 'core/index.html', parameters)
    parameters = {
        'products': products,
        'categories': categories,

        'new_prods': new_prods,
        'f_items': f_new_prods
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


@login_required(login_url='user_login')
def checkout(request):
    if Cart.objects.filter(user=request.user).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        cart_items = Cart.objects.filter(user=request.user)
        len_of_cart = len(Cart.objects.filter(user=request.user))
        if request.method == "POST" and request.POST.get('quantity', False):
            quantity = int(request.POST['quantity'])
            product_slug_filter = request.POST.get('prod-slug', "none")
            inst_product = Product.objects.filter(
                slug=product_slug_filter).first()
            if inst_product:
                cart_item = Cart.objects.filter(
                    user=request.user, product=inst_product).first()
                order_item = OrderItem.objects.filter(
                    user=request.user, product=inst_product).first()
                if cart_item and order_item:
                    cart_item.set_quantity(quantity)
                    order_item.set_quantity(quantity)
                    cart_item.save()
                    order_item.save()
                    return redirect('/cart')
        cart_prod_and_price = []
        total_price = 0
        for item in cart_items:
            total_price += int(item.quantity * item.product.price)
            cart_prod_and_price.append(
                [item, (item.quantity * item.product.price)])

        if request.method == "POST" and request.POST.get('address'):
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            country = request.POST['country']
            zip_code = request.POST['pincode']
            phone = request.POST['phone']

            # setting the cart model with delivery details

            item = cart_items.first()
            item.firstname = first_name
            item.lastname = last_name
            item.Address = address
            item.country = country
            item.zip_code = zip_code
            item.phone = phone

            item.save()
            

            # Payment Gateway

            try:
                order = Order.objects.get(user=request.user, ordered=False)
                # address = checkout.objects.get(user=request.user)
                order_currency = "INR"
                order_receipt = order.order_id
                # notes = {
                #     "street_address": address.street_address,
                #     "apartment_address": address.apartment_address,
                #     "country": address.country.name,
                #     "zip": address.zip,
                # }
                razorpay_order = razorpay_client.order.create(
                    dict(
                        amount=total_price * 100,
                        currency=order_currency,
                        receipt=order_receipt,
                        payment_capture="0",
                    )
                )

                print(razorpay_order["id"])
                order.razorpay_order_id = razorpay_order["id"]
                order.save()
                print("it should render the summary page")

                if Cart.objects.filter(user=request.user).exists():
                    cart = Cart.objects.filter(user=request.user).first()
                    cart.orderID = razorpay_order["id"]
                    cart.save()

                return render(
                    request,
                    "core/checkout.html",
                    {
                        "order": order,
                        "order_id": razorpay_order["id"],
                        "orderId": order.order_id,
                        "final_price": total_price,
                        "razorpay_merchant_id": settings.RAZORPAY_ID,
                        'len_of_cart': len_of_cart, 
                        'cart_prod_and_price': cart_prod_and_price, 
                        'total_price': total_price, 
                        'item': item
                    }
                )

            except Order.DoesNotExist:
                print("Order not Found")
                return HttpResponse("404 error")
            
            # return redirect('/checkout')

        item = cart_items.first()
        if item.country:
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                order_currency = "INR"
                order_receipt = order.order_id
                razorpay_order = razorpay_client.order.create(
                    dict(
                        amount=total_price * 100,
                        currency=order_currency,
                        receipt=order_receipt,
                        payment_capture="0",
                    )
                )

                print(razorpay_order["id"])
                order.razorpay_order_id = razorpay_order["id"]
                order.save()
                print("it should render the summary page")

                return render(
                    request,
                    "core/checkout.html",
                    {
                        "order": order,
                        "order_id": razorpay_order["id"],
                        "orderId": order.order_id,
                        "final_price": total_price,
                        "razorpay_merchant_id": settings.RAZORPAY_ID,
                        'len_of_cart': len_of_cart, 
                        'cart_prod_and_price': cart_prod_and_price, 
                        'total_price': total_price, 
                        'item': item
                    }
                )

            except Order.DoesNotExist:
                print("Order not Found")
                return HttpResponse("404 error")

        return render(request, 'core/checkout.html', {'order': order, 'len_of_cart': len_of_cart, 'cart_prod_and_price': cart_prod_and_price, 'total_price': total_price, 'item': item})


def cart(request):
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user).exists():
            order = Order.objects.get(user=request.user, ordered=False)
            cart_items = Cart.objects.filter(user=request.user)
            len_of_cart = len(Cart.objects.filter(user=request.user))
            if request.method == "POST" and request.POST.get('quantity', False):
                quantity = int(request.POST['quantity'])
                product_slug_filter = request.POST.get('prod-slug', "none")
                inst_product = Product.objects.filter(
                    slug=product_slug_filter).first()
                if inst_product:
                    cart_item = Cart.objects.filter(
                        user=request.user, product=inst_product).first()
                    order_item = OrderItem.objects.filter(
                        user=request.user, product=inst_product).first()
                    if cart_item and order_item:
                        cart_item.set_quantity(quantity)
                        order_item.set_quantity(quantity)
                        cart_item.save()
                        order_item.save()

                        return redirect('/cart')
            cart_prod_and_price = []
            for item in cart_items:
                cart_prod_and_price.append(
                    [item, (item.quantity * item.product.price)])
           
            return render(request, 'core/cart.html', {'order': order, 'len_of_cart': len_of_cart, 'cart_prod_and_price': cart_prod_and_price})
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request, 'core/cart.html', {'message': "Your cart is empty", 'len_of_cart': len_of_cart})
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
    categories = Category.objects.all()

    parameters = {
        "category": category,
        "products": products,
        'categories': categories
    }

    return render(request, "core/shop.html", parameters)


def products(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        ordered_products = Product.objects.exclude(slug=slug)
        recommended_products = ordered_products.order_by("?")[:3]
        reviews = Reviews.objects.filter(product=product)
        if (request.user.is_authenticated):
            len_of_cart = len(Cart.objects.filter(user=request.user))
            return render(request, "core/product-details.html", {'len_of_cart': len_of_cart, 'prodDescp': product, 'reviews': reviews, 'recommended_products': recommended_products})
        return render(request, "core/product-details.html", {'prodDescp': product, 'reviews': reviews, 'recommended_products': recommended_products})

    except Exception as e:
        return HttpResponse("404 Not Found")


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if (request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request, "core/shop.html", {'len_of_cart': len_of_cart, 'products': products, 'categories': categories, })
    return render(request, "core/shop.html", {'products': products, 'categories': categories, })


def contactus(request):
    if (request.user.is_authenticated):
        len_of_cart = len(Cart.objects.filter(user=request.user))
        return render(request, "core/contact-us.html", {'len_of_cart': len_of_cart})
    return render(request, "core/contact-us.html")


def remove_cart_items(request, pk):
    cart_product = Cart.objects.filter(pk=pk)
    cart_product.delete()
    return redirect('cart')


def managecontactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        print(name, email, subject, message)
        contact_details = ContactUs(
            name=name, email=email, subject=subject, message=message)
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


def saveReview(request, slug):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        product = Product.objects.get(slug=slug)
        review_details = Reviews(
            name=name, email=email, review=message, product=product)
        review_details.save()
        return redirect(f"/{slug}")


def search(request):
    query = request.GET.get("query")
    all_products_name = Product.objects.filter(name__icontains=query)
    all_products_desc = Product.objects.filter(desc__icontains=query)
    filtered_prods = all_products_name | all_products_desc
    categories = Category.objects.all()
    params = {"products": filtered_prods,
              'query': query, 'categories': categories, }
    return render(request, "core/shop.html", params)

    

def handlerequest(request):
    try:
        print(request.method)
        if request.method == "POST":
            print("enter1")
            payment_id = request.POST.get("razorpay_payment_id", "")
            print("enter2")
            order_id = request.POST.get("razorpay_order_id", "")
            print("enter3")
            signature = request.POST.get("razorpay_signature", "")
            print(payment_id,order_id,signature)
            cart = Cart.objects.filter(orderID = order_id).first()
            print("enter4")
            if cart:
                order = MyOrders(user = request.user, order = cart)
                order.save()
                cart.isPaid = True 
                cart.save()
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
                print("order found")
            except:
                print("order not found")
                return HttpResponse("505 not found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            print("working............")
            result = razorpay_client.utility.verify_paymen_signature(params_dict)
            if result == None:
                print("woring finally fine.........")
                amount = order_db.get_total_price()
                amount = amount * 100
                payment_status = razorpay_client.payment.capture(payment_id, amount)
                if payment_status is not None:
                    print(payment_status)
                    order_db.ordered = True
                    order_db.save()
                    print("Payment success")
                    request.session[
                        "order_failed"

                    ] = "Unfortunately your order could not be placed, try again"
                    return redirect("/")
                else:
                    order_db.ordered = False
                    order_db.save()
                    return render(request, "paymentfailed.html")
    except:
        return HttpResponse("Error occured")

                
               


    

