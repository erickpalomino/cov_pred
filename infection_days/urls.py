from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('init_db',views.init_database,name="init_db"),
    path('getInfDay',views.getInfectionDay,name="getInfectionDay"),
]
