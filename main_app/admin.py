from django.contrib import admin

# Register your models here.
from .models import Meal, Food, Profile
admin.site.register(Meal)
admin.site.register(Food)
admin.site.register(Profile)