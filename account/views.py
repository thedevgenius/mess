from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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

