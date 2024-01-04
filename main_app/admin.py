from django.contrib import admin

# Register your models here.
from .models import Meal, Food
admin.site.register(Meal)
admin.site.register(Food)