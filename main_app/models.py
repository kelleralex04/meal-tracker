from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

MEALCHOICE = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('A', 'Additional Meal'),
)

class Meal(models.Model):
    food = models.CharField()
    amount = models.IntegerField()
    date = models.DateField(default=datetime.now, blank=True)
    favorited = models.BooleanField(default=False)
    mealType = models.CharField(
        max_length=1,
        choices=MEALCHOICE,
        default=MEALCHOICE[0][0]
    )

class Profile(models.Model):
    age = models.IntegerField()
    height = models.IntegerField()
    initWeight = models.IntegerField()
    goalWeight = models.IntegerField()

class BodyData(models.Model):
    weight = models.IntegerField()
    date = models.DateField(default=datetime.now, blank=True)