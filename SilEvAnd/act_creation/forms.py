from django import forms
from .models import Act, Conformity, Boss, StickPlace


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
            'control_sticks_number': forms.Textarea(attrs={'class': 'auto-resize-textarea', 'rows': '1'}),
            'act_number': forms.NumberInput(attrs={'size': '10', 'maxlength': '10'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получить объект Conformity с названием 'Cоотв.' или создать его, если не существует
        default_conformity, created = Conformity.objects.get_or_create(conformity='Соотв.')
        self.fields['conformity'].initial = default_conformity.pk

class ActDataInput(forms.Form):
    act_number = forms.ModelChoiceField(queryset=Act.objects.all().order_by('-act_number'), label='№ Акта')
    boss = forms.ModelChoiceField(queryset=Boss.objects.all(), label='Лицо утверждающее акт')
    stick_place = forms.ModelChoiceField(queryset=StickPlace.objects.all(), label='Платформа ИА')
