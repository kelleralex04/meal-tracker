from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendarIndex, name='calendar'),
    path('calendar/m<int:curMonth>d<int:i>y<int:curYear>/', views.calendarDetail, name='day'),
    path('calendar/m<int:curMonth>d<int:i>y<int:curYear>/meal/', views.calendarMeal, name='daymeal'),
    path('calendar/m<int:curMonth>d<int:i>y<int:curYear>/body/', views.calendarBody, name='daybody'),
    path('accounts/signup/', views.signup, name="signup"),
]
