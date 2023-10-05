from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from mill.models import *
from account.models import Member

# Create your views here.
def Home(request):
    members = Member.objects.all()
    data = {
        'members' : members
    }
    return render(request, 'index.html', data)

def save_mill(request):
    if request.method == 'POST':
        
        count = Member.objects.count()

        for i in range(1, count+1):
            date = request.POST.get(f'mill_date{i}')
            new_member = request.POST.get(f'mill_person{i}')
            mill = request.POST.get(f'mill_mill{i}')
            new_bazar = request.POST.get(f'mill_bazar{i}')
            member = Member.objects.get(pk=new_member)
            bazar = Member.objects.get(pk=new_bazar)
            mill = Mill(
                    date=date,
                    member=member,
                    mill=mill,
                    bazar=bazar
                )
            mill.save()

        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def Dashboard(request):
    return render(request, 'dashboard.html')


def get_mills(request):
    posts = Mill.objects.all()
    posts_html = render_to_string('content.html', {'posts': posts})

    return JsonResponse({'posts_html': posts_html})

