from django import forms
from django.core.exceptions import ValidationError
from .models import ControlJournal


class ControlJournalInput(forms.ModelForm):
    class Meta:
        model = ControlJournal
        fields = ['short_slot_name',
                  'user_many',
                  'act',
                  'notice']
        widgets = {
            'short_slot_name': forms.Textarea(attrs={'cols':30, 'rows': 2}),
            'act': forms.Textarea(attrs={'cols':30, 'rows': 2}),
            'notice': forms.Textarea(attrs={'cols':30, 'rows': 2})
        }