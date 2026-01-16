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
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
                success_message: 'Заявка успешно зарегистрирована!'
        else:
            danger_message = 'У вас недостаточно прав для регистрации заявки'
    context = (
        {'applications': applications,
         'page_obj': page_obj,
         'form': form,
         'success_message': success_message,
         'danger_message': danger_message
         }
    )
    return render(request, 'application.html', context)

def application_del(request, pk):
    applications = Application.objects.all().order_by('-application_number')
    app_del = Application.objects.get(pk=pk)
    app_del.delete()
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ApplicationInput()
    context = (
        {'applications': applications,
         'form': form,
         'page_obj': page_obj
         }
    )
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
    context = (
        {
        'form': form,
        'applications': app_change,
        'success_message': success_message
         }
    )
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
    context = (
        {
            'form': form,
            'declarants': declarants,
            'success_message': success_message,
            'danger_message': danger_message
        }
    )
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
    context = (
        {
            'form': form,
            'declarant': declarant_change,
            'success_message': success_message
        }
    )
    return render(request, 'declarant_change.html', context)

def network_graph(request):
    network_graph_data = NetworkGraph.objects.all()
    context = (
        {
            'network_graph': network_graph_data
        }
    )
    return render(request, 'network_graph.html', context)

def network_graph_change(request,pk):
    network_graph_data = NetworkGraph.objects.get(pk=pk)
    success_message, danger_message = '', ''
    form = NetworkGraphInput()
    if request.method == 'POST':
        form = NetworkGraphInput(request.POST, instance=network_graph_data)
        if form.is_valid():
            form.save()
            form = NetworkGraphInput()
            success_message = 'Изменения в сетевой график внесены успешно'
    else:
        form = NetworkGraphInput(instance=network_graph_data)
    context = (
        {
            'form': form,
            'network_graph_data': network_graph_data,
            'success_message': success_message
        }
    )
    return render(request, 'network_graph_change.html', context)


def declarant_del(request, pk):
    declarants = Declarant.objects.all().order_by('name')
    decl_del = Declarant.objects.get(pk=pk)
    decl_del.delete()
    form = DeclarantInput()
    context = (
        {
            'form': form,
            'declarants': declarants
        }
    )
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
