from django import forms
from .models import Act, Conformity, Boss, StickPlace, Manufacturer


class ActInput(forms.ModelForm):
    is_deleted = forms.BooleanField(
        required=False,
        initial=False,
        label="Удалить",
        help_text="Поставьте галочку если эту строку нужно удалить из формы. Затем нажмите 'Сохранить черновик'"
    )
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
    boss = forms.ModelChoiceField(queryset=Boss.objects.all(), label='лицо, утверждающее акт')
    stick_place = forms.ModelChoiceField(queryset=StickPlace.objects.all(), label='платформу ИА')
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), blank=True, label='производителя, если Novomatic')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_manufacturer = Manufacturer.objects.get(name='Из реестра')
        self.fields['manufacturer'].initial = default_manufacturer.pk
