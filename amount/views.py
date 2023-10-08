from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from mill.models import *
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def ShowDiposit(request):
    current_date = timezone.now()
    diposits = Diposit.objects.filter(date__month=current_date.month, date__year=current_date.year, member_id=request.user.id)
    total = Diposit.objects.filter(date__month=current_date.month, date__year=current_date.year, member_id=request.user.id).aggregate(Sum('amount'))
    total_amount = total['amount__sum']

    common_exps = Diposit.objects.filter(date__month=current_date.month, date__year=current_date.year, purpose__in=('O', 'G'))
    common_exps_amount = common_exps.aggregate(Sum('amount'))
    total_exp_emount = common_exps_amount['amount__sum']

    data = {
        'diposits' : diposits,
        'total_amount' : total_amount,
        'common_exps' : common_exps,
        'total_exp_emount' : total_exp_emount
    }
    return render(request, 'show-diposit.html', data)

@login_required
def AddDiposit(request):
    if request.method == 'POST':
        date = request.POST['date']
        member = Member.objects.get(pk=request.user.id)
        reasone = request.POST['reasone']
        amount = request.POST['amount']
        Diposit.objects.create(
            date=date,
            member=member,
            purpose=reasone,
            amount=amount
        )
        messages.success(request, 'Amount diposited to your account !')
        return redirect('diposits')
    
    data = {
        
    }
    return render(request, 'add-diposit.html', data)

@login_required
def AddExp(request):
    if request.method == 'POST':
        diposit_id = request.POST['diposit_id']
        diposit = Diposit.objects.get(pk=diposit_id)
        title=request.POST['exp_title']
        Exp.objects.create(
            name=title,
            diposit=diposit
        )
        diposit = get_object_or_404(Diposit, pk=diposit_id)
        diposit.ststus = True
        diposit.save()
        #print(diposit.ststus)
    return redirect('expenditures')

@login_required
def Expenditures(request):
    current_date = timezone.now()
    diposits = Diposit.objects.filter(date__month=current_date.month-1, date__year=current_date.year, member_id=request.user.id).exclude(purpose='M')

    est_exps = Exp.objects.filter(diposit__date__month=current_date.month, diposit__date__year=current_date.year, diposit__purpose__in=('O','G'))
    total_est_amount = est_exps.aggregate(Sum('diposit__amount'))['diposit__amount__sum']

    oth_exps = Exp.objects.filter(diposit__date__month=current_date.month, diposit__date__year=current_date.year).exclude(diposit__purpose__in=('O', 'G'))
    total_oth_exps = oth_exps.aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    
    data = {
        'diposits' : diposits,
        'est_exps' : est_exps,
        'total_est_amount' : total_est_amount,
        'oth_exps' : oth_exps,
        'total_oth_exps' : total_oth_exps
    }
    return render(request, 'exp.html', data)


@login_required
def Bill(request):
    current = timezone.now()
    month = current.month
    if month == 12:
        year = current.year-1
    else:
        year = current.year
    if month == 1:
        month = 12
    else:
        month = month-1
    
    total_mill = Mill.objects.filter(date__month=month, date__year=year).aggregate(Sum('mill'))['mill__sum']

    total_bazar_cost = Bazar.objects.filter(date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum']

    total_extra = Exp.objects.filter(diposit__date__month=month, diposit__date__year=year).exclude(diposit__purpose__in=('O', 'G')).aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    if total_extra:
        total_extra = total_extra
    else:
        total_extra = 0

    total_cost = total_bazar_cost+total_extra
    mill_charge = round((total_cost/total_mill), 2)

    est = Exp.objects.filter(diposit__date__month=month, diposit__date__year=year, diposit__purpose__in=('O', 'G')).aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    common_est = CommonExp.objects.get(date__month=month, date__year=year)
    total_common_est = common_est.electric + common_est.rice + common_est.coock
    
    total_est = est+total_common_est
    number_of_member = Member.objects.filter(is_active=True).count()
    est_charge = round((total_est/number_of_member), 2)

    
    members = Member.objects.all()

    if common_est is not None:
        for member in members:
            my_mill = Mill.objects.filter(date__month=month, date__year=year, member_id=member.id).aggregate(Sum('mill'))['mill__sum']
            print(my_mill)
            



    return render(request, 'bill.html')