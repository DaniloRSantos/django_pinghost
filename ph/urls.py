from django.urls import path
from ph import views

urlpatterns = [
    path('', views.index),
    path('check_availability', views.check_availability, name='check_availability'),
]