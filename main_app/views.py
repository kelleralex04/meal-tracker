from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import calendar

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

def calendarDetail(request, curMonth, i, curYear):
    month = months[curMonth - 1]
    return render(request, 'day.html', {
        'curMonth': month, 'curDay': i, 'curYear': curYear
    })
