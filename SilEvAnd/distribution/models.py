from django.db import models
from django.contrib.auth.models import User



class ControlJournal(models.Model):
    short_slot_name = models.TextField(max_length=200, blank=True, null=True, verbose_name='Модели ИА')
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='control_journal')
    act = models.TextField(max_length=200, blank=True, null=True, verbose_name='Акт ТО')
    notice = models.TextField(max_length=200, blank=True, null=True, verbose_name='Примечание')
    user_many = models.ManyToManyField(User, related_name='control_journals_as_users', verbose_name='Исполнители')
    def __str__(self):
        return str(self.application)



