from django.shortcuts import render, redirect
from .models import Registry, Act, Conformity
import openpyxl
from django.contrib.auth.decorators import permission_required
from distribution.models import ControlJournal
from .forms import ActInput
from django.forms import formset_factory
import json

@permission_required('act_creation.view_registry')
def registry(request):
    registries = Registry.objects.all()
    list_keys = ['number', 'model', 'version', 'manufacturer']
    param_dict = {key : request.GET.get(key) for key in list_keys}
    for param, value in param_dict.items():
        if value:
            filter_name = f'{param}__icontains'
            registries = registries.filter(**{filter_name: value})
    context = {
        'registries': registries,
        'number_get': param_dict['number'],
        'model_get': param_dict['model'],
        'version_get': param_dict['version'],
        'manufacturer_get': param_dict['manufacturer']
         }
    return render(request, 'registry.html', context)

@permission_required('act_creation.add_registry')
def registry_input(request):
    wb = openpyxl.load_workbook(
        'D:\PythonCreateActTOProject\Reestr\Реестр ИА.xlsx')
    ws = wb.active
    for row in ws.iter_rows(min_row=2):
        registry_new = Registry(
            number=row[0].value,
            model=row[1].value,
            version=row[2].value,
            manufacturer=row[3].value
        )
        registry_new.save()
    registries = Registry.objects.all()
    context = {
            'registries': registries
        }
    return render(request, 'registry.html', context)

@permission_required('act_creation.view_act')
def slot_machine_data(request):
    slot_machines_data = Act.objects.all().order_by('-act_number')
    list_keys = [
        'act_number', 'application', 'control_sticks_number',
        'declarant', 'result', 'model', 'version', 'slot_number',
        'reg_number', 'board_number'
    ]
    param_dict = {_: request.GET.get(_) for _ in list_keys}
    for key, value in param_dict.items():
        if value:
            if key == 'application':
                filter_name = f'distribution__application__application_number__icontains'
            elif key == 'declarant':
                filter_name = f'distribution__application__declarant__name__icontains'
            elif key == 'model' or key == 'version':
                filter_name = f'model_registry__{key}__icontains'
            elif key == 'reg_number':
                filter_name = f'model_registry__number__icontains'
            else:
                filter_name = f'{key}__icontains'
            slot_machines_data = slot_machines_data.filter(**{filter_name: str(value)})


    context = {
            'slot_machines_data': slot_machines_data,
            'act_number': param_dict['act_number'],
            'application': param_dict['application'],
            'control_sticks_number': param_dict['control_sticks_number'],
            'declarant': param_dict['declarant'],
            'result': param_dict['result'],
            'model': param_dict['model'],
            'version': param_dict['version'],
            'slot_number': param_dict['slot_number'],
            'reg_number': param_dict['reg_number'],
            'board_number': param_dict['board_number']
        }

    return render(request, 'slot_machine_data.html', context)

@permission_required('act_creation.add_act')
def s_m_data_input(request, pk):
    users_application = ControlJournal.objects.get(pk=pk)
    slot_machines_data = Act.objects.all().order_by('-act_number')
    conformity = Conformity.objects.all()
    registry = Registry.objects.all()
    ActFormSet = formset_factory(ActInput,extra=1)
    success_message = ''

    initial_session_data = None
    if request.method == 'GET':
        data = request.session.get('act_formset_data')
        if data:
            initial_session_data = data
            for form in initial_session_data:
                form['conformity'] = conformity.get(conformity=form['conformity'])
                form['model_registry'] = registry.get(number=form['model_registry'])
        formset = ActFormSet(initial=initial_session_data)

    elif request.method == 'POST':
        formset = ActFormSet(request.POST)

        if formset.is_valid():
            if 'save_draft' in request.POST.keys():
                cleaned_data_list = [form.cleaned_data for form in formset if form.cleaned_data]
                for form in cleaned_data_list:
                    form['conformity'] = str(form['conformity'])
                    form['model_registry'] = str(form['model_registry'])
                print(cleaned_data_list)
                request.session['act_formset_data'] = cleaned_data_list
                success_message = 'Черновик успешно сохранен в сессии.'
            elif 'save_form' in request.POST.keys():
                last_act = slot_machines_data.first().act_number
                formset = ActFormSet(request.POST)
                if formset.is_valid():
                    act_number = None
                    for form in formset:
                        if form.cleaned_data and form.cleaned_data.get('act_number'):
                            act_number = form.cleaned_data.get('act_number')
                    if act_number is None:
                        act_number = last_act + 1
                    for form in formset:
                        if form.cleaned_data:
                            slot_machines_data_new = Act(
                                act_number=act_number,
                                distribution=users_application,
                                control_sticks_number=form.cleaned_data['control_sticks_number'],
                                conformity=form.cleaned_data['conformity'],
                                model_registry=form.cleaned_data['model_registry'],
                                slot_number=form.cleaned_data['slot_number'],
                                board_number=form.cleaned_data['board_number']
                            )
                            slot_machines_data_new.save()
                            formset = ActFormSet()
                            request.session.pop('act_formset_data', None)
                            success_message = 'Акт успешно добавлен в журнал'

    list_keys = [
        'act_number', 'application', 'control_sticks_number',
        'declarant', 'result', 'model', 'version', 'slot_number',
        'reg_number', 'board_number'
    ]
    param_dict = {_: request.GET.get(_) for _ in list_keys}
    for key, value in param_dict.items():
        if value:
            if key == 'application':
                filter_name = f'distribution__application__application_number__icontains'
            elif key == 'declarant':
                filter_name = f'distribution__application__declarant__name__icontains'
            elif key == 'model' or key == 'version':
                filter_name = f'model_registry__{key}__icontains'
            elif key == 'reg_number':
                filter_name = f'model_registry__number__icontains'
            else:
                filter_name = f'{key}__icontains'
            slot_machines_data = slot_machines_data.filter(**{filter_name: str(value)})

    context = (
        {
            'slot_machines_data': slot_machines_data,
            'users_application': users_application,
            'formset': formset,
            'success_message': success_message,
            'act_number': param_dict['act_number'],
            'application': param_dict['application'],
            'control_sticks_number': param_dict['control_sticks_number'],
            'declarant': param_dict['declarant'],
            'result': param_dict['result'],
            'model': param_dict['model'],
            'version': param_dict['version'],
            'slot_number': param_dict['slot_number'],
            'reg_number': param_dict['reg_number'],
            'board_number': param_dict['board_number'],
            'empty_form': formset.empty_form
        }
    )
    return render(request, 's_m_data_input.html', context)

@permission_required('act_creation.view_act')
def act_creation(request):
    user_now = request.user
    slot_machines_data = Act.objects.all().order_by('act_number')
    users_applications = ControlJournal.objects.filter(user=user_now).filter(application__status__in=['4']).order_by('-id')
    context = (
        {
            'slot_machines_data': slot_machines_data,
            'users_applications': users_applications,
            'user_now': user_now
        }
    )
    return render(request, 'act_creation.html', context)
