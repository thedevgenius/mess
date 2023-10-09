from .models import *
from mill.models import *
from django.utils import timezone
from django.db.models import Sum, Q, Count

def get_prev_month():
    current = timezone.now()
    month = current.month
    if month == 1:
        month = 12
    else:
        month = month-1
    return month

def get_prev_year():
    current = timezone.now()
    month = current.month
    if month == 12:
        year = current.year-1
    else:
        year = current.year
    return year


def get_millcharge():
    month = get_prev_month()
    year = get_prev_year()
    
    total_mill = Mill.objects.filter(date__month=month, date__year=year).aggregate(Sum('mill'))['mill__sum']

    total_bazar_cost = Bazar.objects.filter(date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum']

    total_extra = Exp.objects.filter(diposit__date__month=month, diposit__date__year=year).exclude(diposit__purpose__in=('O', 'G')).aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    if total_extra:
        total_extra = total_extra
    else:
        total_extra = 0

    total_cost = total_bazar_cost+total_extra
    mill_charge = round((total_cost/total_mill), 2)

    return mill_charge

def get_est_charge():
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
    est = Exp.objects.filter(diposit__date__month=month, diposit__date__year=year, diposit__purpose__in=('O', 'G')).aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    common_est = CommonExp.objects.get(month=month, year=year)
    total_common_est = common_est.cook+common_est.electric+common_est.rice
    #print(total_common_est)
    
    total_est = est+total_common_est
    number_of_member = Member.objects.filter(is_active=True).count()
    est_charge = round((total_est/number_of_member), 2)

    return est_charge