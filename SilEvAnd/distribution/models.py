from django.db import models
from django.contrib.auth.models import User



class ControlJournal(models.Model):
    short_slot_name = models.TextField(max_length=200, blank=True, null=True, verbose_name='Модели ИА')
    place = models.CharField(max_length=50, blank=True, null=True, verbose_name='Место проведения ТО')
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='control_journal')
    act = models.TextField(max_length=200, blank=True, null=True, verbose_name='Акт ТО')
    notice = models.TextField(max_length=200, blank=True, null=True, verbose_name='Примечание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Исполнитель')
    def __str__(self):
        return str(self.application)



