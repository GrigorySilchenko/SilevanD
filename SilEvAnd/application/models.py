from django.db import models
from django.utils import timezone


class Application(models.Model):
    application_number = models.IntegerField()
    created_on = models.DateField(default=timezone.now, blank=True, null=True)
    application_number_belgiss = models.IntegerField(blank=True, null=True, verbose_name='Входящий номер БелГИСС')
    date_belgiss = models.DateField(blank=True, null=True, verbose_name='Дата входящего номера БелГИСС')
    num_of_mach = models.IntegerField(verbose_name='Количество ИА')
    bill_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер счета')
    bill_date = models.DateField(blank=True, null=True, verbose_name='Дата счета')
    payment = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Сумма')
    payment_document = models.CharField(max_length=10, blank=True, null=True, verbose_name='Номер п/п')
    payment_date = models.DateField(blank=True, null=True, verbose_name='Дата п/п')
    pdf = models.FileField(verbose_name='PDF', upload_to='PDF/', blank=True, null=True)
    declarant = models.ForeignKey('Declarant', on_delete=models.CASCADE, related_name='applications', verbose_name='Заявитель')
    place = models.CharField(max_length=50, default='Минск', blank=True, null=True, verbose_name='Место проведения ТО')
    notice = models.TextField(max_length=200, default='', blank=True, null=True, verbose_name='Примечание')
    status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='applications')
    def __str__(self):
        return str(self.application_number)

class Declarant(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование заявителя')
    address = models.TextField(max_length=500, verbose_name='Юридический адрес')
    unp = models.IntegerField(verbose_name='УНП')
    def __str__(self):
        return self.name

class Status(models.Model):
    status = models.CharField(max_length=200)
    def __str__(self):
        return self.status

class NetworkGraph(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='network_graph', verbose_name='Заявка')
    control_journal = models.ForeignKey('distribution.ControlJournal', on_delete=models.CASCADE, related_name='network_graph', blank=True, null=True, verbose_name='Акт по заявке')
    recalculation = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Перерасчет')
    notice_recalculation = models.TextField(max_length=200, default='', blank=True, null=True, verbose_name='Основание для перерасчета')
    act_send_date = models.TextField(max_length=50, default='', blank=True, null=True, verbose_name='Дата направления акта')
    final_notice = models.TextField(max_length=200, default='', blank=True, null=True, verbose_name='Примечание')
    app_closed = models.BooleanField(default=False, blank=True, null=True, verbose_name='')
    def __str__(self):
        return str(self.application)

