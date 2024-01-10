from django.forms import ModelForm
from .models import Meal, MealFoodItem, BodyData, Food, Profile
from django.contrib.auth.forms import UserCreationForm

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

class FoodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'style': 'color: white'})
        self.fields['calories'].widget.attrs.update({'style': 'color: white'})
        self.fields['carbs'].widget.attrs.update({'style': 'color: white'})
        self.fields['protein'].widget.attrs.update({'style': 'color: white'})
        self.fields['amount'].widget.attrs.update({'style': 'color: white'})

    class Meta:
        model = Food
        fields = ['name', 'calories', 'carbs', 'protein', 'amount']

class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update({'style': 'color: white'})
        self.fields['lastname'].widget.attrs.update({'style': 'color: white'})
        self.fields['age'].widget.attrs.update({'style': 'color: white'})
        self.fields['height'].widget.attrs.update({'style': 'color: white'})
        self.fields['initWeight'].widget.attrs.update({'style': 'color: white'})
        self.fields['goalWeight'].widget.attrs.update({'style': 'color: white'})

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'age', 'height', 'initWeight', 'goalWeight']

class NewUserCreationForm(UserCreationForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'style': 'color: white'})
            self.fields['password1'].widget.attrs.update({'style': 'color: white'})
            self.fields['password2'].widget.attrs.update({'style': 'color: white'})