import openpyxl
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Application, Status, Declarant, NetworkGraph
from .forms import ApplicationInput, DeclarantInput, NetworkGraphInput
from datetime import date
from django.core.paginator import Paginator


def home(request):
    return render(request, 'home.html')

def status_giving(cleaned_data):
    if cleaned_data['payment_document']:
        status = Status.objects.get(pk=8)
    elif cleaned_data['application_number_belgiss'] and cleaned_data['bill_number']:
        status = Status.objects.get(pk=2)
    elif cleaned_data['application_number_belgiss'] and not cleaned_data['bill_number']:
        status = Status.objects.get(pk=1)
    else:
        status = Status.objects.get(pk=7)
    return status

@permission_required('application.view_application')
def application(request):
    applications = Application.objects.all().order_by('-application_number')
    last_app = applications.first().application_number

    if last_app:
        application_number_new = last_app + 1
    else:
        application_number_new = 1
    created_on_new = date.today()
    form = ApplicationInput()
    success_message, danger_message = '', ''

    if request.method == 'POST':
        if request.user.has_perm('application.add_application'):
            form = ApplicationInput(request.POST, request.FILES)
            if form.is_valid():
                status = status_giving(form.cleaned_data)
                application_new = Application(
                    application_number=application_number_new,
                    created_on=created_on_new,
                    application_number_belgiss=form.cleaned_data['application_number_belgiss'],
                    date_belgiss=form.cleaned_data['date_belgiss'],
                    num_of_mach=form.cleaned_data['num_of_mach'],
                    bill_number=form.cleaned_data['bill_number'],
                    bill_date=form.cleaned_data['bill_date'],
                    payment=form.cleaned_data['payment'],
                    payment_document=form.cleaned_data['payment_document'],
                    payment_date=form.cleaned_data['payment_date'],
                    pdf=form.cleaned_data['pdf'],
                    place=form.cleaned_data['place'],
                    notice=form.cleaned_data['notice'],
                    declarant=form.cleaned_data['declarant'],
                    status=status
                )
                application_new.save()
                network_graph_new = NetworkGraph.objects.create(application=application_new)
                form = ApplicationInput()
                success_message = 'Заявка успешно зарегистрирована!'
        else:
            danger_message = 'У вас недостаточно прав для регистрации заявки'

    if request.GET:
        filter_dict = request.GET
        for key, value in filter_dict.items():
            if value:
                if key == 'declarant':
                    filter_name = f'declarant__name__icontains'
                else:
                    filter_name = f'{key}__icontains'
                applications = applications.filter(**{filter_name: str(value)})
    else:
        filter_dict = dict()

    paginator = Paginator(applications, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'success_message': success_message,
        'danger_message': danger_message,
        'filter_dict': filter_dict
        }

    return render(request, 'application.html', context)

def application_del(request, pk):
    applications = Application.objects.all().order_by('-application_number')
    app_del = Application.objects.get(pk=pk)
    app_del.delete()
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ApplicationInput()

    context = {
        'applications': applications,
        'form': form,
        'page_obj': page_obj
        }

    return render(request, 'application.html', context)

@permission_required('application.change_application')
def application_change(request, pk):
    app_change = Application.objects.get(pk=pk)
    success_message = ''
    status = app_change.status.id
    if request.method == 'POST':
        form = ApplicationInput(request.POST, request.FILES, instance=app_change)
        if form.is_valid():
            if status == 1 or status == 2 or status == 7:
                status = status_giving(form.cleaned_data)
                form.instance.status = status
            form.save()
            success_message = 'Заявка успешно изменена!'
    else:
        form = ApplicationInput(instance=app_change)

    context = {
        'form': form,
        'applications': app_change,
        'success_message': success_message
         }

    return render(request, 'application_change.html', context)

@permission_required('application.view_declarant')
def declarant(request):
    declarants = Declarant.objects.all().order_by('name')
    success_message, danger_message = '', ''
    form = DeclarantInput()
    if request.method  == 'POST':
        if request.user.has_perm('application.add_declarant'):
            form = DeclarantInput(request.POST)
            if form.is_valid():
                form.save()
                form = DeclarantInput()
                success_message = 'Заявитель успешно добавлен в базу'
        else:
            danger_message = 'У вас недостаточно прав для добавления нового заявителя'
    context = {
        'form': form,
        'declarants': declarants,
        'success_message': success_message,
        'danger_message': danger_message
        }
    return render(request, 'declarant.html', context)

@permission_required('application.change_declarant')
def declarant_change(request, pk):
    declarant_change = Declarant.objects.get(pk=pk)
    success_message = ''
    if request.method == 'POST':
        form = DeclarantInput(request.POST, instance=declarant_change)
        if form.is_valid():
            form.save()
            success_message = 'Данные заявителя успешно изменены!'
    else:
        form = DeclarantInput(instance=declarant_change)

    context = {
        'form': form,
        'declarant': declarant_change,
        'success_message': success_message
        }

    return render(request, 'declarant_change.html', context)

@permission_required('application.view_networkgraph')
def network_graph(request):
    network_graph_data = NetworkGraph.objects.all().order_by('-application__application_number')

    if 'reset' in request.GET:
        request.session.pop('net_graph_filters', None)
        return redirect('network_graph')

    filter_data = request.session.get('net_graph_filters')
    filter_dict = request.GET
    if not filter_data:
        if request.GET:
            param_dict = filter_dict
            request.session['net_graph_filters'] = param_dict
        else:
            param_dict = dict()
    else:
        if request.GET and filter_data != filter_dict:
            param_dict = filter_dict
            request.session['net_graph_filters'] = param_dict
        else:
            param_dict = filter_data

    date_get_start = param_dict.get('date_from')
    date_get_end = param_dict.get('date_to')
    if date_get_start:
        start = date.fromisoformat(date_get_start)
        if date_get_end:
            end = date.fromisoformat(date_get_end)
        else:
            end = date.today().isoformat()
        network_graph_data = network_graph_data.filter(application__created_on__range=(start, end))
    else:
        if date_get_end:
            end = date.fromisoformat(date_get_end)
        else:
            end = date.today().isoformat()
        network_graph_data = network_graph_data.filter(application__created_on__lte=end)

    is_final_notice = param_dict.get('is_final_notice')
    if is_final_notice:
        network_graph_data = network_graph_data.exclude(final_notice='')

    for key, value in param_dict.items():
        if key == 'date_from' or key == 'date_to' or key == 'is_final_notice':
            pass
        elif value:
            if key == 'application_number' or key == 'bill_number' or key == 'payment' or key == 'payment_document' or key == 'num_of_mach':
                filter_name = f'application__{key}__icontains'
            elif key == 'declarant':
                filter_name = f'application__declarant__name__icontains'
            elif key == 'act':
                filter_name = f'control_journal__{key}__icontains'
            elif key == 'app_closed':
                filter_name = key
                if value == 'True':
                    network_graph_data = network_graph_data.filter(final_notice='')
            else:
                filter_name = f'{key}__icontains'
            network_graph_data = network_graph_data.filter(**{filter_name: value})

    context = {
        'network_graph': network_graph_data,
        'app_closed': param_dict.get('app_closed'),
        'date_from': param_dict.get('date_from'),
        'date_to': param_dict.get('date_to'),
        'is_final_notice': param_dict.get('is_final_notice'),
        'declarant':param_dict.get('declarant'),
        'application_number':param_dict.get('application_number'),
        'bill_number':param_dict.get('bill_number'),
        'payment':param_dict.get('payment'),
        'payment_document':param_dict.get('payment_document'),
        'num_of_mach':param_dict.get('num_of_mach'),
        'act':param_dict.get('act'),
        'recalculation': param_dict.get('recalculation'),
        'num_exclude_mach': param_dict.get('num_exclude_mach'),
        'notice_recalculation': param_dict.get('notice_recalculation'),
        'act_send_date': param_dict.get('act_send_date'),
        'final_notice': param_dict.get('final_notice')
        }

    return render(request, 'network_graph.html', context)

@permission_required('application.change_networkgraph')
def network_graph_change(request,pk):
    network_graph_data = NetworkGraph.objects.get(pk=pk)
    success_message, danger_message = '', ''
    form = NetworkGraphInput()
    if request.method == 'POST':
        form = NetworkGraphInput(request.POST, instance=network_graph_data)
        if form.is_valid():
            form.save()
            # form = NetworkGraphInput()
            success_message = 'Изменения в сетевой график внесены успешно'
    else:
        form = NetworkGraphInput(instance=network_graph_data)
    context = {
        'form': form,
        'network_graph_data': network_graph_data,
        'success_message': success_message
        }

    return render(request, 'network_graph_change.html', context)


def declarant_del(request, pk):
    declarants = Declarant.objects.all().order_by('name')
    decl_del = Declarant.objects.get(pk=pk)
    decl_del.delete()
    form = DeclarantInput()

    context = {
        'form': form,
        'declarants': declarants
        }

    return render(request, 'declarant.html', context)

def declarant_input():
    wb = openpyxl.load_workbook(
        'D:\PythonCreateActTOProject\ActTO\База заявителей с адресами 23.12.2025.xlsx')
    ws = wb.active
    for row in ws.iter_rows(min_row=2):
        declarant_new = Declarant(
            name=row[0].value,
            address=row[1].value,
            unp=row[2].value
        )
        declarant_new.save()
