from django.contrib.auth.decorators import permission_required
from django.db.models import Sum
from django.shortcuts import render
from .models import ControlJournal
from application.models import Application, Status, NetworkGraph
from .forms import ControlJournalInput
from datetime import date



@permission_required('distribution.view_controljournal')
def distribution(request):
    distributions = ControlJournal.objects.all().order_by('-application')
    applications = Application.objects.filter(status__in=['2', '1', '7', '8']).order_by('id')

    app_get = request.GET.get('app')
    if app_get:
        distributions = distributions.filter(application__application_number__contains=str(app_get))

    date_get_start = request.GET.get('date_start')
    date_get_end = request.GET.get('date_end')
    if date_get_start and date_get_end:
        start = date.fromisoformat(date_get_start)
        end = date.fromisoformat(date_get_end)
        distributions = distributions.filter(application__created_on__range=(start, end))

    declarant_get = request.GET.get('declarant')
    if declarant_get:
        distributions = distributions.filter(application__declarant__name__icontains=declarant_get)

    act_get = request.GET.get('act')
    if act_get:
        distributions = distributions.filter(act__icontains=act_get)

    user_get = request.GET.get('user')
    if user_get:
        distributions = distributions.filter(user__username__icontains=user_get)

    mach_total = distributions.aggregate(total=Sum('application__num_of_mach')).get('total')

    context = (
        {
            'distributions': distributions,
            'app_get': app_get,
            'date_get_start': date_get_start,
            'date_get_end': date_get_end,
            'declarant_get': declarant_get,
            'act_get': act_get,
            'user_get': user_get,
            'applications': applications,
            'mach_total': mach_total
         }
    )
    return render(request, 'distribution.html', context)

@permission_required('distribution.view_controljournal')
def application_distribution(request, pk):
    application = Application.objects.get(pk=pk)
    net_graph = NetworkGraph.objects.get(application_id=pk)
    form = ControlJournalInput()
    success_message = ''
    distributions = ControlJournal.objects.all().order_by('-application')
    if request.method == 'POST':
        form = ControlJournalInput(request.POST)
        if form.is_valid():
            status = Status.objects.get(id=4)
            application.status = status
            application.save()
            distribution_new = ControlJournal(
                short_slot_name=form.cleaned_data['short_slot_name'],
                user=form.cleaned_data['user'],
                application=application,
                act=form.cleaned_data['act'],
                notice=form.cleaned_data['notice']
            )
            distribution_new.save()
            net_graph.control_journal = distribution_new
            net_graph.save()
            form = ControlJournalInput()
            success_message = 'Заявка добавлена в журнал и отправлена исполнителю'
    context = (
        {
        'form': form,
        'application': application,
        'success_message': success_message,
        'distributions': distributions
         }
    )

    return render(request, 'application_distribution.html', context)


@permission_required('distribution.change_controljournal')
def distribution_change(request, pk):
    distributions = ControlJournal.objects.all().order_by('-application')
    distr_change = ControlJournal.objects.get(pk=pk)
    app_id = distr_change.application.id
    print(app_id)
    net_graph = NetworkGraph.objects.get(application_id=app_id)
    form = ControlJournalInput()
    success_message = ''
    if request.method == 'POST':
        form = ControlJournalInput(request.POST, instance=distr_change)
        if form.is_valid():
            control_journal_new = form.save()
            net_graph.control_journal = control_journal_new
            net_graph.save()
            success_message = 'Журнал "Контроль ИА" успешно изменен.'
    else:
        form = ControlJournalInput(instance=distr_change)

    context = (
        {
        'form': form,
        'distributions': distributions,
        'distribution': distr_change,
        'success_message': success_message
         }
    )
    return render(request, 'distribution_change.html', context)
