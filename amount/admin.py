from django.contrib import admin
from .models import *
# Register your models here.

class CommonAdmin(admin.ModelAdmin):
    list_display =('year', 'month')

class BillAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'name', 'mill', 'mill_cost', 'establish', 'total', 'diposit', 'due')

admin.site.register(Diposit)
admin.site.register(Exp)
admin.site.register(CommonExp, CommonAdmin)
admin.site.register(Bill, BillAdmin)