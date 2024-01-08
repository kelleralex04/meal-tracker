from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import calendar
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Meal, Food, Profile, BodyData, MealFoodItem
from django.views.generic import ListView, DetailView
from django import forms
from .forms import MealForm, MealFoodItemForm, BodyDataForm



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
    meal = Meal.objects.filter(date__gte=datetime(curYear, curMonth, 1), date__lte=datetime(curYear, curMonth, lastDateofMonth[1]))
    mealdates = set()
    for m in meal:
        mealdates.add(m.date.day)

    return render(request, 'calendar.html', {
        'curMonthText': curMonthText, 'curYear': curYear, 'curMonth': curMonth, 'curDay': curDay, 'firstInactiveDays': firstInactiveDays, 'activeDays': activeDays, 
        'lastDateOfPrevMonth': lastDateOfPrevMonth, 'lastInactiveDays': lastInactiveDays, 'todayDay': todayDay, 'todayMonth': todayMonth, 'todayYear': todayYear, 'mealdates': mealdates
    })

@login_required
def calendarDetail(request, curMonth, i, curYear):
    month = months[curMonth - 1]
    return render(request, 'day.html', {
        'month': month, 'curDay': i, 'curYear': curYear, 'curMonth': curMonth,
    })

@login_required
def calendarMeal(request, curMonth, curDay, curYear):
    meals = Meal.objects.filter(date=datetime(curYear,curMonth,curDay))
    foods = Food.objects.all()
    month = months[curMonth - 1]
    meal_form = MealForm()
    meal_food_item_form = MealFoodItemForm()
    return render(request, 'daymeal.html', {
        'curMonth': curMonth, 'month': month, 'curDay': curDay, 'curYear': curYear, 'meals': meals, 'meal_food_item_form': meal_food_item_form, 'foods': foods, 'meal_form': meal_form
    })

def assoc_food(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    curMeal = Meal.objects.filter(date=curDate, mealType=request.POST['mealType'])
    f = Food.objects.get(name=request.POST['foodChoice'])
    mfi = MealFoodItem(name=f.name, calories=f.calories, carbs=f.carbs, protein=f.protein, amount=f.amount, servings=request.POST['servings'])
    mfi.save()
    fall = Food.objects.all()
    print(fall)
    if len(curMeal):
        curMeal[0].food.add(mfi)
    else:
        m = Meal(date=curDate, mealType=request.POST['mealType'])
        m.save()
        m.food.add(mfi)
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/meal')

@login_required
def calendarBody(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    month = months[curMonth - 1]
    weight = BodyData.objects.filter(date=curDate)
    bodyDataForm = BodyDataForm()
    if len(weight):
        w = weight[0].weight
    else:
        w = None
    return render(request, 'daybody.html', {
        'curMonth': curMonth, 'month': month, 'curDay': curDay, 'curYear': curYear, 'weight': w, 'body_data_create': bodyDataForm,
    })

def calendarBodyCreate(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    w = BodyData(date=curDate, weight=request.POST['weight'])
    w.save()
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/body')

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
            return redirect('profile_create')
        else:
            error_message = 'You made an oopsie doopsie, go ahead and try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class FoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'style': 'color: white'})
        self.fields['calories'].widget.attrs.update({'style': 'color: white'})
        self.fields['carbs'].widget.attrs.update({'style': 'color: white'})
        self.fields['protein'].widget.attrs.update({'style': 'color: white'})
        self.fields['amount'].widget.attrs.update({'style': 'color: white'})

    class Meta:
        model = Food
        fields = '__all__'

class FoodCreate(LoginRequiredMixin, CreateView):
    form_class = FoodForm
    model = Food
    success_url = '/foods'

class FoodList(LoginRequiredMixin, ListView):
    model = Food

class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    fields = '__all__'

class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = '/foods'

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['firstname', 'lastname', 'age', 'height', 'initWeight', 'goalWeight']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/calendar'

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = '__all__'

