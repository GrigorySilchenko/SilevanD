from django import forms
from django.core.exceptions import ValidationError
from .models import Application, Declarant


class ApplicationInput(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['declarant',
                  'application_number_belgiss',
                  'date_belgiss',
                  'num_of_mach',
                  'bill_number',
                  'bill_date',
                  'payment',
                  'payment_document',
                  'payment_date',
                  'pdf']
        widgets = {
            'date_belgiss': forms.DateInput(attrs={'type': 'date'}),
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'pdf': forms.ClearableFileInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        application_number_belgiss_value = cleaned_data.get('application_number_belgiss')
        date_belgiss_value = cleaned_data.get('date_belgiss')
        bill_number_value = cleaned_data.get('bill_number')
        bill_date_value = cleaned_data.get('bill_date')
        if application_number_belgiss_value and not date_belgiss_value:
            self.add_error('date_belgiss', 'Заполните поле даты входящего номера БелГИСС')
        elif not application_number_belgiss_value and date_belgiss_value:
            self.add_error('application_number_belgiss', 'Заполните поле входящего номера БелГИСС')
        if bill_number_value and not bill_date_value:
            self.add_error('bill_date', 'Заполните поле даты счета')
        elif not bill_number_value and bill_date_value:
            self.add_error('bill_number', 'Заполните поле номера счета')
        return cleaned_data

class DeclarantInput(forms.ModelForm):
    class Meta:
        model = Declarant
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'cols':30, 'rows': 2}),
            'address': forms.Textarea(attrs={'cols': 30, 'rows': 3})
        }