from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from mill.models import *
from django.utils import timezone
from django.db.models import Sum, Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import *
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


    


def MyBill(request):
    month = get_prev_month()
    year = get_prev_year()

    try:
        cal_btn = CommonExp.objects.get(month=month, year=year)
    except CommonExp.DoesNotExist:
        cal_btn = None
    
    data = {
        'cal_btn' : cal_btn
    }
    return render(request, 'bill.html', data)




@login_required
def Bills(request):
    if request.method == 'POST':
        month = get_prev_month()
        year = get_prev_year()
        mill_charge = get_millcharge()
        est_charge = get_est_charge()
                
        members = Member.objects.filter(is_active=True)
        for member in members:
            my_mill = Mill.objects.filter(date__month=month, date__year=year, member_id=member.id).aggregate(Sum('mill'))['mill__sum']
            mill_cost = my_mill*mill_charge
            totalcost = round((mill_cost+est_charge), 2)
            my_diposit = Diposit.objects.filter(date__month=month, date__year=year, member_id=member.id).aggregate(Sum('amount'))['amount__sum']
            if my_diposit == None:
                my_diposit = 0
            due=round((totalcost-my_diposit), 2)
            try:
                bill = Bill.objects.get(month=month, year=year, name_id=member.id)
                bill.mill=my_mill                
                bill.establish = est_charge
                bill.total = totalcost
                bill.due = due
                bill.diposit = my_diposit
                bill.save()
            except Bill.DoesNotExist:
                name = Member.objects.get(pk=member.id)
                Bill.objects.create(
                    month=month,
                    year=year,
                    name=name,
                    mill=my_mill,
                    mill_cost=mill_cost,
                    establish=est_charge,
                    total=totalcost,
                    diposit=my_diposit,
                    due=due
                )
    return redirect(request.META.get('HTTP_REFERER', 'home'))