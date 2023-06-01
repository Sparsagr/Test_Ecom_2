from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from core.models import Profile
from core.models import *
from django.contrib import messages
# Create your views here.


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_obj = User.objects.filter(username=username)

        if not user_obj.exists():

            messages.error(request, "Account doesn't exists")
            return redirect("/accounts/user_login")

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Account Not Verified")
            return redirect("/accounts/user_login")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            messages.error(request, "Incorrect credentials")
            return redirect("/accounts/user_login")

    return render(request, "core/login.html")


def user_register(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email_address = request.POST["email_address"]
            password = request.POST["password"]

            new_user = User.objects.create_user(
                username=username, email=email_address)
            new_user.set_password(str(password))

            new_user.save()
            messages.error(
                request, "Check you Email for verrifying your registered account")

            return redirect("/accounts/user_login")
        except Exception as e:
            return HttpResponse("Username or Email already exists!")

    return render(request, "core/login.html")


def user_logout(request):
    logout(request)
    return redirect("user_login")


def activate(request, token):
    try:
        profile = Profile.objects.get(email_token=token)
        profile.is_email_verified = True
        profile.save()
        messages.success(request, "Account Verified")
        return redirect("/accounts/user_login")
    except Exception as e:
        messages.error(request, "Invalid Token")
        return redirect("/accounts/user_login")
