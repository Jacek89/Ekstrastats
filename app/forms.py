from django import forms
from datetime import date
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from crispy_forms.bootstrap import PrependedText
from .models import Team
from django.utils.html import format_html


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


class TeamModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, team):
        return format_html(f'<img src="{team.logo}" class="table-logo">{team.name}')


class PoisPredictForm(forms.Form):
    teams_extra = Team.objects.filter(ekstraklasa=True)

    team_home = TeamModelChoiceField(
        queryset=teams_extra,
        empty_label="Team Home"
    )

    team_away = forms.ModelChoiceField(
        queryset=teams_extra,
        empty_label="Team Away"
    )

    def __init__(self, *args, **kwargs):
        super(PoisPredictForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'pois-form'
        self.helper.form_show_labels = False
        self.helper.form_action = reverse('analysis')
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            Div(
                Div('team_home', css_class='col-md-3'),
                Div('team_away', css_class='col-md-3'),
                Div(Submit('submit', 'Predict'), css_class='col-md-2'),
                css_class='row pt-3',
                )
        )
