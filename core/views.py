from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def Dashboard(request):
    return render(request, 'dashboard.html')