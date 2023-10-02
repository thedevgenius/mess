from django import forms
from .models import *

class AddMillForm(forms.ModelForm):
    
    class Meta:
        model = Mill
        fields = '__all__'
        widgets = {
            'date' : forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'})
        }
