from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from mill.models import *
from amount.models import *
from account.models import Member
from django.utils import timezone
from django.db.models import Sum, Count

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
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def Dashboard(request):
    date = timezone.now()
    total_mill = Mill.objects.filter(date__month=date.month, date__year=date.year, member_id=request.user.id).aggregate(Sum('mill'))['mill__sum']
    
    total_bazar = Bazar.objects.filter(date__month=date.month, date__year=date.year, member_id=request.user.id).count()
    my_bazars = Bazar.objects.filter(date__month=date.month, date__year=date.year, member_id=request.user.id)
    bazar_amount = Bazar.objects.filter(date__month=date.month, date__year=date.year, member_id=request.user.id).aggregate(Sum('amount'))['amount__sum']
    if bazar_amount is None:
        bazar_amount = 0

    diposits = Diposit.objects.filter(date__month=date.month, date__year=date.year, member_id=request.user.id)
    diposit_amount = diposits.aggregate(Sum('amount'))['amount__sum']
    if diposit_amount is None:
        diposit_amount = 0

    total_diposit = 0
    total_diposit = diposit_amount

    data = {
        'total_mill' : total_mill,
        'total_bazar' : total_bazar,
        'my_bazars' : my_bazars,
        'bazar_amount' : bazar_amount,
        'diposits' : diposits,
        'diposit_amount' : diposit_amount,
        'total_diposit' : total_diposit
    }
    return render(request, 'dashboard.html', data)


