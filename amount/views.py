from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib import messages
# Create your views here.

def ShowDiposit(request):
    current_date = timezone.now()
    diposits = Diposit.objects.filter(date__month=current_date.month, date__year=current_date.year)
    total = Diposit.objects.aggregate(Sum('amount'))
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