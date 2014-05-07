# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from djzbar.utils.informix import do_sql

BINARY_CHOICES = (
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
)

class SicklecellForm(forms.Form):
    waive = forms.BooleanField(
        required=False
    )
    proof = forms.BooleanField(
        required=False
    )

    results = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

    def clean(self):
        """
        Student must choose one or the other of two checkboxes,
        and the results if they choose "proof".
        """
        cleaned_data = self.cleaned_data

        if not cleaned_data["waive"] and not cleaned_data["proof"]:
            raise forms.ValidationError(
                "Please check one of the checkboxes below."
            )
        elif cleaned_data["proof"] and not cleaned_data["results"]:
            raise forms.ValidationError(
                '''
                Please indicate whether your test results were
                "positive or "negative".
                '''
            )

        return cleaned_data

class PrivacyForm(forms.Form):
    ncaa_tool = forms.BooleanField()
    medical_insurance = forms.BooleanField()
    news_media = forms.BooleanField()
    parents_guardians = forms.BooleanField()
    disclose_records = forms.BooleanField()

class ReportingForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )

class RiskForm(forms.Form):
    agree = forms.BooleanField(
        required=True
    )
