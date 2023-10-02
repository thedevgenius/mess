from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def AddMill(request):
    if request.method == 'POST':
        form = AddMillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddMillForm()

    data = {
        'form' : form
    }

    return render(request, 'add-mill.html', data)