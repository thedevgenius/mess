from django.db import models
from datetime import datetime
from account.models import *
# Create your models here.

ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
MILL_NUMBER = (
    (ZERO, '0'),
    (ONE, '1'),
    (TWO, '2'),
    (THREE, '3'),
    (FOUR, '4')
)

class Mill(models.Model):
    date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    mill = models.IntegerField(choices=MILL_NUMBER, default=2)
    bazar = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='bazar_person')

    class Meta:
        unique_together = ('date', 'member',)

