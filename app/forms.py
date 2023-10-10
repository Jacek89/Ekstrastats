from django import forms
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_forms.bootstrap import PrependedText

class TableDate(forms.Form):
    date_from = forms.DateField(label='from:',
                                initial="2023-07-01",
                                widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    date_to = forms.DateField(label='to:',
                              initial=date.today,
                              widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(TableDate, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'table-form'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div(PrependedText('date_from', "from:"), css_class='col-md-5'),
                Div(PrependedText('date_to', "to:"), css_class='col-md-5'),
                Div(Submit('submit', 'Filter'), css_class='col-md-2'),
                css_class='row pt-3',
                )
        )