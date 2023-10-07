from django.contrib import admin
from .models import *
# Register your models here.
class MillAdmin(admin.ModelAdmin):
    list_display = ('date', 'member', 'mill', 'bazar')

admin.site.register(Mill, MillAdmin)

# class BazarAdmin(admin.ModelAdmin):
#     list_display = ('date', 'member', 'amount')

admin.site.register(Bazar)