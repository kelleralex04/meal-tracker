from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import calendar
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Meal, Food, Profile, BodyData, MealFoodItem
from django.views.generic import ListView, DetailView
from .forms import MealForm, MealFoodItemForm, BodyDataForm, FoodForm, ProfileForm, NewUserCreationForm
from django.contrib.auth.models import User



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

    bothdates = set()
    user = User.objects.get(id=request.user.id)

    curMonthText = months[curMonth - 1]
    meal = Meal.objects.filter(date__gte=datetime(curYear, curMonth, 1), date__lte=datetime(curYear, curMonth, lastDateofMonth[1]), user=user)
    mealdates = set()
    for m in meal:
        mealdates.add(m.date.day)

    weight = BodyData.objects.filter(date__gte=datetime(curYear, curMonth, 1), date__lte=datetime(curYear, curMonth, lastDateofMonth[1]), user=user)
    weightdates = set()
    for w in weight:
        if w.date.day in mealdates:
            mealdates.remove(w.date.day)
            bothdates.add(w.date.day)
        else:
            weightdates.add(w.date.day)

    return render(request, 'calendar.html', {
        'curMonthText': curMonthText, 'curYear': curYear, 'curMonth': curMonth, 'curDay': curDay, 'firstInactiveDays': firstInactiveDays, 'activeDays': activeDays, 
        'lastDateOfPrevMonth': lastDateOfPrevMonth, 'lastInactiveDays': lastInactiveDays, 'todayDay': todayDay, 'todayMonth': todayMonth, 'todayYear': todayYear, 'mealdates': mealdates,
        'weightdates': weightdates, 'bothdates': bothdates
    })

@login_required
def calendarDetail(request, curMonth, i, curYear):
    month = months[curMonth - 1]
    return render(request, 'day.html', {
        'month': month, 'curDay': i, 'curYear': curYear, 'curMonth': curMonth,
    })

@login_required
def calendarMeal(request, curMonth, curDay, curYear):
    user = User.objects.get(id=request.user.id)
    meals = Meal.objects.filter(date=datetime(curYear,curMonth,curDay), user=user)
    foods = Food.objects.filter(user=user)
    totalCalories = 0
    totalCarbs = 0
    totalProtein = 0
    for meal in meals:
        for food in meal.food.all():
            totalCalories += food.calories
            totalCarbs += food.carbs
            totalProtein += food.protein
    month = months[curMonth - 1]
    meal_form = MealForm()
    meal_food_item_form = MealFoodItemForm()
    return render(request, 'daymeal.html', {
        'curMonth': curMonth, 'month': month, 'curDay': curDay, 'curYear': curYear, 'meals': meals, 'meal_food_item_form': meal_food_item_form, 'foods': foods, 'meal_form': meal_form,
        'totalCalories': totalCalories, 'totalCarbs': totalCarbs, 'totalProtein': totalProtein
    })

@login_required
def assoc_food(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    user = User.objects.get(id=request.user.id)
    curMeal = Meal.objects.filter(date=curDate, mealType=request.POST['mealType'], user=user)
    f = Food.objects.get(name=request.POST['foodChoice'])
    servings = int(request.POST['servings'])
    mfi = MealFoodItem(name=f.name, calories=(f.calories * servings), carbs=(f.carbs * servings), protein=(f.protein * servings), amount=(f.amount * servings), servings=servings)
    mfi.save()
    curFoods = []
    if len(curMeal) and len(curMeal[0].food.all()):
        for i in curMeal[0].food.all().values():
            curFoods.append(i['name'])
        if f.name in curFoods:
            repeat = curMeal[0].food.get(name=f.name)
            repeat.calories += f.calories * servings
            repeat.carbs += f.carbs * servings
            repeat.protein += f.protein * servings
            repeat.amount += f.amount * servings
            repeat.servings += servings
            repeat.save()
        else:
            curMeal[0].food.add(mfi)
    else:
        m = Meal(date=curDate, mealType=request.POST['mealType'], user=user)
        m.save()
        m.food.add(mfi)
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/meal')

@login_required
def remove_food(request, curMonth, curDay, curYear, meal_id, food_id):
    m = Meal.objects.get(id=meal_id)
    m.food.remove(food_id)
    MealFoodItem.objects.get(id=food_id).delete()
    if not len(m.food.all()):
        m.delete()

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

@login_required
def calendarBodyCreate(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    user = User.objects.get(id=request.user.id)
    w = BodyData(date=curDate, weight=request.POST['weight'], user=user)
    w.save()
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/body')    

@login_required
def calendarBodyUpdate(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    user = User.objects.get(id=request.user.id)
    weight = BodyData.objects.get(date=curDate, user=user)
    weight.weight = request.POST["weight"]
    weight.save()
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/body')

@login_required
def calendarBodyDelete(request, curMonth, curDay, curYear):
    curDate = datetime(curYear, curMonth, curDay)
    user = User.objects.get(id=request.user.id)
    BodyData.objects.get(date=curDate, user=user).delete()
    return redirect(f'/calendar/m{curMonth}d{curDay}y{curYear}/body')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('profile_create')
        else:
            error_message = 'You made an oopsie doopsie, go ahead and try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = NewUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food
    form_class = FoodForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/foods'

@login_required
def foodIndex(request):
    foods = Food.objects.filter(user=request.user)
    return render(request, 'foods_index.html', {
        'foods': foods
    })

class FoodUpdate(LoginRequiredMixin, UpdateView):
    form_class = FoodForm
    model = Food
    success_url = '/foods'

class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = '/foods'

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/calendar'

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Profile

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = Profile
