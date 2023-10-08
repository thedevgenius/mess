from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import *

# Create your views here.
def Registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        password = request.POST['password']
        user = Member.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            password = password,
        )
        login(request, user)
        return redirect('home')

    else:
        pass
    return render(request, 'registration.html')


def Login(request):
    if request.method == 'POST':
        next_url = request.POST.get('next')
        phone=request.POST['phone']
        password=request.POST['password']
        user = authenticate(phone=phone, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        
    return render(request, 'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Logout(request):
    logout(request)
    return redirect('home')
