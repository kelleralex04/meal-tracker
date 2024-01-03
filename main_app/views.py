from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import calendar
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Meal

date = datetime.now()
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [1, 2, 3, 4, 5, 6, 0]
curDay = date.day
curMonth = date.month
curYear = date.year
todayDay = curDay
todayMonth = curMonth
todayYear = curYear

def home(request):
    return render(request, 'home.html')

@login_required
def calendarIndex(request):
    global curMonth, curYear
    if request.POST:
        if 'prev' in request.POST:
            curMonth -= 1
        else:
            curMonth += 1

    if curMonth > 12:
        curYear += 1
        curMonth = 1
    elif curMonth < 1:
        curYear -= 1
        curMonth = 12

    firstDayOfMonth = days[datetime(curYear, curMonth, 1).weekday()]
    lastDateofMonth = calendar.monthrange(curYear, curMonth)
    lastDayOfMonth = days[datetime(curYear, curMonth, lastDateofMonth[1]).weekday()]
    lastDateOfPrevMonth = (datetime(curYear, curMonth, 1) - timedelta(days = 1)).day
    firstInactiveDays = []
    activeDays = []
    lastInactiveDays = []

    for i in range(firstDayOfMonth, 0, -1):
        firstInactiveDays.append(lastDateOfPrevMonth + 1 - i)

    for i in range(lastDateofMonth[1]):
        activeDays.append(i + 1)

    if lastDayOfMonth < 7:
        for i in range(6 - lastDayOfMonth):
            lastInactiveDays.append(i + 1)

    curMonthText = months[curMonth - 1]

    return render(request, 'calendar.html', {
        'curMonthText': curMonthText, 'curYear': curYear, 'curMonth': curMonth, 'curDay': curDay, 'firstInactiveDays': firstInactiveDays, 'activeDays': activeDays, 
        'lastDateOfPrevMonth': lastDateOfPrevMonth, 'lastInactiveDays': lastInactiveDays, 'todayDay': todayDay, 'todayMonth': todayMonth, 'todayYear': todayYear 
    })

@login_required
def calendarDetail(request, curMonth, i, curYear):
    month = months[curMonth - 1]
    return render(request, 'day.html', {
        'curMonth': month, 'curDay': i, 'curYear': curYear
    })

@login_required
def calendarMeal(request, curMonth, i, curYear):
    meal = Meal.objects.filter(date=datetime(curYear,curMonth,i))
    month = months[curMonth - 1]
    return render(request, 'daymeal.html', {
        'curMonth': month, 'curDay': i, 'curYear': curYear, 'meal': meal
    })

@login_required
def calendarBody(request, curMonth, i, curYear):
    month = months[curMonth - 1]
    return render(request, 'daybody.html', {
        'curMonth': month, 'curDay': i, 'curYear': curYear
    })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('calendar')
    else:
      error_message = 'You made an oopsie doopsie, go ahead and try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)