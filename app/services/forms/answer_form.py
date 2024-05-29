from django import forms
from django.core.exceptions import ValidationError


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter your answer here.."
    )

    def clean(self):
        return self.cleaned_data

    def clean_text(self):
        text = self.cleaned_data['text']
        return text
