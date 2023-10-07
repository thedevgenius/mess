from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .forms import *
import datetime
from amount.models import *

# Create your views here.
def AddMill(request):
    members = Member.objects.all()
    
    if request.method == 'POST':
        count = Member.objects.count()
        try:
            mill_values = []
            for i in range(1, count+1):
                date = request.POST.get('mill_date')
                new_member = request.POST.get(f'mill_person{i}')
                mill = int(request.POST.get(f'mill_mill{i}'))
                new_bazar = request.user.id
                member = Member.objects.get(pk=new_member)
                bazar = Member.objects.get(pk=new_bazar)
                mill_values.append(mill)

                mill = Mill(
                        date=date,
                        member=member,
                        mill=mill,
                        bazar=bazar
                    )
                mill.save()

            bazar_date = request.POST.get('mill_date')
            total_mill = 0
            for j in mill_values:
                total_mill += j
            total_amount = (total_mill*10)+20
            member = Member.objects.get(pk=request.user.id)
            Bazar.objects.create(
                date=bazar_date,
                member=member,
                amount=total_amount
            )
            Diposit.objects.create(
                date=bazar_date,
                member=member,
                amount=total_amount
            )
            
            #print(total_amount)
        except IntegrityError:
            messages.error(request, 'Mill for this date aready added.')
            return redirect('addmill')
        messages.success(request, 'Mill Added !')
        return redirect('showmill')

    data = {
        'members' : members
    }

    return render(request, 'add-mill.html', data)


def ShowMill(request):
    # today = datetime.date.today()
    # first_day = today.replace(day=1)
    # last_day = (first_day + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    # dates = [first_day + datetime.timedelta(days=i) for i in range((last_day - first_day).days + 1)]

    members = Member.objects.all()
    mills = Mill.objects.all()
    bazars = Bazar.objects.all().order_by('date')
    data = {
        'members' : members,
        'mills' : mills,
        'bazars' : bazars
    }
    return render(request, 'show-mill.html', data)