from django.db import models
from datetime import datetime
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
    

class CommonExp(models.Model):
    date = models.DateField()
    electric = models.IntegerField()
    rice = models.IntegerField()
    coock = models.IntegerField()

    def __str__(self):
        return str(self.date)
    

        
