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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servings'].widget.attrs.update({'style': 'color: white'})

class BodyDataForm(ModelForm):
    class Meta:
        model = BodyData
        fields = ['weight']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['weight'].widget.attrs.update({'style': 'color: white'})