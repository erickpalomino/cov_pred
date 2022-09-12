from django.db import models


# Create your models here.
class InfectionDay(models.Model):
  date=models.DateField(name='date',primary_key=True)
  real_infection=models.IntegerField(name='real_infection',null=True)
  pred_infection=models.IntegerField(name='pred_infection',null=True)
  inputs=models.ManyToManyField('self')
  class Meta:
    ordering=['date']
  def __str__(self):
    return f'InfectionDay(date={self.date},real_infection={self.real_infection},pred_infection={self.pred_infection},inputs={self.inputs})'

