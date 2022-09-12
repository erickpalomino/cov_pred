from datetime import datetime
import dateutil.parser
from django.shortcuts import render
from django.http import HttpResponse

from infection_days.models import InfectionDay
# Create your views here.
format_str = '%Y-%m-%d' # The format

def index(request):
  return HttpResponse("Hello")

def init_database(request):
  import pandas
  import matplotlib.pyplot as plt
  dataset = pandas.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', engine='python')
  from pandas.core.frame import DataFrame
  ds_filtered=dataset[dataset['location']=='Peru']
  ds_filtered=DataFrame(data={"new_cases":ds_filtered['new_cases'].values},index=ds_filtered['date'].values)
  ds_filtered=ds_filtered.fillna(method='bfill').fillna(method='ffill')
  for i in range(len(ds_filtered)):
    infection_day=InfectionDay(date=datetime.strptime(str(ds_filtered.iloc[i].name),format_str),real_infection=ds_filtered.iloc[i][0])
    infection_day.save()
  print(InfectionDay.objects.all())
  return HttpResponse("DB ready")

def getInfectionDay(request):
  date=request.GET['date']
  infectionDay=InfectionDay.objects.get(pk=datetime.strptime(str(date),format_str))
  return HttpResponse(str(infectionDay))