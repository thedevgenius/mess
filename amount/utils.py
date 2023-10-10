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


def get_month_name(number):
    if number == 1:
        name = 'January'
    elif number == 2:
        name = 'February'
    elif number == 3:
        name = 'March'
    elif number == 4:
        name = 'April'
    elif number == 5:
        name = 'May'
    elif number == 6:
        name = 'June'
    elif number == 7:
        name = 'July'
    elif number == 8:
        name = 'August'
    elif number == 9:
        name = 'September'
    elif number == 10:
        name = 'October'
    elif number == 11:
        name = 'November'
    elif number == 12:
        name = 'December'
    
    return name


def get_millcharge():
    month = get_prev_month()
    year = get_prev_year()
    
    total_mill = Mill.objects.filter(date__month=month, date__year=year).aggregate(Sum('mill'))['mill__sum']
    total_bazar_cost = Bazar.objects.filter(date__month=month, date__year=year).aggregate(Sum('amount'))['amount__sum']

    common_exp = CommonExp.objects.get(month=month, year=year)
    rice = common_exp.rice
    
    total_cost = total_bazar_cost+rice
    mill_charge = round((total_cost/total_mill), 3)

    return mill_charge

def get_est_charge():
    month = get_prev_month()
    year = get_prev_year()


    est = Exp.objects.filter(diposit__date__month=month, diposit__date__year=year).aggregate(Sum('diposit__amount'))['diposit__amount__sum']
    common_est = CommonExp.objects.get(month=month, year=year)
    total_common_est = common_est.cook+common_est.electric
    #print(total_common_est)
    
    total_est = est+total_common_est
    number_of_member = Member.objects.filter(is_active=True).count()
    est_charge = round((total_est/number_of_member), 3)

    return est_charge