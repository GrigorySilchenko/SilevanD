from django.db import models


class Registry(models.Model):
    number = models.CharField(max_length=10)
    model = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    manufacturer = models.CharField(max_length=500)
    def __str__(self):
        return self.number

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    stick_place = models.ForeignKey('StickPlace', on_delete=models.CASCADE, related_name='manufacturer', blank=True, null=True)
    def __str__(self):
        return self.name

class Boss(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class StickPlace(models.Model):
    board_name = models.CharField(max_length=100)
    stick_place = models.TextField(max_length=500)
    def __str__(self):
        return self.board_name

class Conformity(models.Model):
    conformity = models.CharField(max_length=20)
    def __str__(self):
        return self.conformity

class Act(models.Model):
    act_number = models.IntegerField(blank=True, null=True, verbose_name='№ Акта')
    distribution = models.ForeignKey('distribution.ControlJournal', on_delete=models.CASCADE, related_name='act_to')
    control_sticks_number = models.TextField(max_length=500, blank=True, null=True, verbose_name='Номера средств контроля')
    conformity = models.ForeignKey('Conformity', on_delete=models.CASCADE, related_name='manufacturer',
                                   blank=True, null=True, verbose_name='Результат')
    model_registry = models.ForeignKey('Registry', on_delete=models.CASCADE, verbose_name='Номер по реестру')
    slot_number = models.CharField(max_length=100, verbose_name='Серийный номер ИА')
    board_number = models.CharField(max_length=50, verbose_name='Номер платы')
    def __str__(self):
        return str(self.act_number)
