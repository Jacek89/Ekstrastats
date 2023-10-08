from django import forms
from datetime import date




class TableDate(forms.Form):
    date_from = forms.DateField(label='from:',
                                initial="2023-07-01",
                                widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    date_to = forms.DateField(label='to:',
                              initial=date.today,
                              widget=forms.widgets.DateInput(attrs={'type': 'date'}))
