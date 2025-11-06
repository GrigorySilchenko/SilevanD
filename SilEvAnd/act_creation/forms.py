from django import forms
from .models import Act, Conformity
from django.forms import modelformset_factory

class ActInput(forms.ModelForm):
    class Meta:
        model = Act
        fields = ['act_number',
                  'control_sticks_number',
                  'conformity',
                  'model_registry',
                  'slot_number',
                  'board_number']
        widgets = {
            'control_sticks_number': forms.Textarea(attrs={'cols': 10, 'rows': 4}),
            'act_number': forms.NumberInput(attrs={'size': '10', 'maxlength': '10'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получить объект Conformity с названием 'соотв.' или создать его, если не существует
        default_conformity, created = Conformity.objects.get_or_create(conformity='Соотв.')
        self.fields['conformity'].initial = default_conformity.pk

