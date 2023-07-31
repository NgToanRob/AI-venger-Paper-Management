from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request):
    return render(request, "Authentication/home.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1 != pass2:
            return HttpResponse(
                "Your password and confirm password are not the same!!!"
            )
        else:
            my_user = User.objects.create_user(
                username=username, email=email, password=pass1
            )
            my_user.save()
            return redirect("login")

    return render(request, "Authentication/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, "Authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
