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
    date = models.DateField(default=datetime.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255, choices=DIPOSIT_PURPOSE, default="M")
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)
    
