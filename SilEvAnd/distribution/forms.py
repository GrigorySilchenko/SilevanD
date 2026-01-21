from django import forms
from django.contrib.auth.models import User
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group_workers = 'workers'
        group_users = User.objects.filter(groups__name=group_workers)
        self.fields['user_many'].queryset = group_users
