from django.forms import ModelForm
from .models import Meal, MealFoodItem, BodyData

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['mealType']

class MealFoodItemForm(ModelForm):
    class Meta:
        model = MealFoodItem
        fields = ['servings']

class BodyDataForm(ModelForm):
    class Meta:
        model = BodyData
        fields = ['weight']