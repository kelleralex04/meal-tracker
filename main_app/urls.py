from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendarIndex, name='calendar'),
    path('calendar/m<int:curMonth>d<int:i>y<int:curYear>/', views.calendarDetail, name='day'),
    path('calendar/m<int:curMonth>d<int:curDay>y<int:curYear>/meal/', views.calendarMeal, name='daymeal'),
    path('calendar/m<int:curMonth>d<int:curDay>y<int:curYear>/meal/assoc_food', views.assoc_food, name='assoc_food'),
    path('calendar/m<int:curMonth>d<int:curDay>y<int:curYear>/body/', views.calendarBody, name='daybody'),
    path('calendar/m<int:curMonth>d<int:curDay>y<int:curYear>/body/create', views.calendarBodyCreate, name='daybody_create'),
    path('accounts/signup/', views.signup, name="signup"),
    path('foods/', views.FoodList.as_view(), name="foods_list"),
    path('foods/create/', views.FoodCreate.as_view(), name="foods_create"),
    path('foods/<int:pk>/update/', views.FoodUpdate.as_view(), name='foods_update'),
    path('foods/<int:pk>/delete/', views.FoodDelete.as_view(), name='foods_delete'),
    path('profile/create/', views.ProfileCreate.as_view(), name='profile_create'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
]
