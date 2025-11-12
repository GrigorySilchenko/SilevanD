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
    pdf = models.FileField(verbose_name='PDF', upload_to='PDF/', blank=True, null=True)
    declarant = models.ForeignKey('Declarant', on_delete=models.CASCADE, related_name='applications', verbose_name='Заявитель')
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
