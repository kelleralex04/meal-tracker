from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendarIndex, name='calendar'),
    path('calendar/m<int:curMonth>d<int:i>y<int:curYear>', views.calendarDetail, name='day'),
]

