from django import forms
from .models import *

class DipositAddForm(forms.ModelForm):
    
    class Meta:
        model = Diposit
        fields = '__all__'

        widgets = {
            'date' : forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'})
        }