from django.db import models
from datetime import datetime
from django.utils import timezone
from account.models import *
# Create your models here.

class Diposit(models.Model):
    DIPOSIT_PURPOSE = [
        ("M", "Mill"),
        ("G", "Gas"),
        ("O", "Oil"),
        ("V", "Ginger & Garlic"),
        ("C", "Chilli"),
    ]
    # STATUS_CHOICE = [
    #     ()
    # ]
    date = models.DateField(default=datetime.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255, choices=DIPOSIT_PURPOSE, default="M")
    ststus = models.BooleanField(default=False)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)
    
class Exp(models.Model):
    name = models.CharField(max_length=255, default='')
    diposit = models.ForeignKey(Diposit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

MONTH_CHOICE = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]
current_year = timezone.now().year

class CommonExp(models.Model):
    month = models.CharField(max_length=2, choices=MONTH_CHOICE, default='1')
    year = models.IntegerField(default=current_year)
    electric = models.IntegerField(null=True, blank=True)
    rice = models.IntegerField(null=True, blank=True)
    cook = models.IntegerField(null=True, blank=True)
    billed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('month', 'year')
    
    def __str__(self):
        return str(self.month)

    
class Bill(models.Model):
    month = models.CharField(max_length=2, choices=MONTH_CHOICE, default='1')
    year = models.IntegerField(default=current_year)
    name = models.ForeignKey(Member, on_delete=models.CASCADE)
    mill = models.IntegerField()
    mill_cost = models.FloatField()
    establish = models.FloatField()
    total = models.FloatField()
    diposit = models.IntegerField(default=0)
    due = models.FloatField()

    class Meta:
        unique_together = ('month', 'year', 'name')

    def __str__(self):
        return str(self.name)