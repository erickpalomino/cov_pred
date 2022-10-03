import datetime
import statistics
from math import trunc
import numpy as np
from time import strptime
import dateutil.parser
from django.shortcuts import render
from django.http import HttpResponse
from infection_days.models import Info
import tensorflow
keras=tensorflow.keras

from infection_days.models import InfectionDay
# Create your views here.
format_str = '%Y-%m-%d' # The format

def format_date(datestr):
  return datetime.strptime(str(datestr),format_str)

def save_last_date(datestr):
  info=Info.objects.get(pk=1)
  info.last_predicted=format_date(str(datestr))
  info.save()

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
    infection_day=InfectionDay(date=format_date(ds_filtered.iloc[i].name),real_infection=ds_filtered.iloc[i][0])
    infection_day.save()
  save_last_date(ds_filtered.iloc[-1].name)
  return HttpResponse("DB ready")

def getInfectionDay(request):
  date=request.GET['date']
  infectionDay=InfectionDay.objects.get(pk=format_date(date))
  return HttpResponse(str(infectionDay))

def predict(request):
  last_day=Info.objects.get(pk=1).last_predicted
  next_day=last_day+datetime.timedelta(days=1)
  #day=next_day
  day=datetime.date(day=1,month=9,year=2022)
  input_reshaped=reshape_input(day)
  model=keras.models.load_model('cov.h5')
  res=model.predict(input_reshaped)
  res=res.reshape(-1)
  print(res)
  res=np.round(res)
  print(np.round(res))
  return HttpResponse(str.format('Day: {} will be {} infecteds',day,res[0]))
  
def reshape_input(date):
  input=[]
  for i in range(14):
    input.append(InfectionDay.objects.get(pk=date-datetime.timedelta(14-i)).real_infection)
  mean= statistics.mean(input)
  std=statistics.stdev(input)
  input.append(mean)
  input.append(std)
  array=np.array(input)
  array=array.reshape(-1,16,1)
  print(array)
  return array