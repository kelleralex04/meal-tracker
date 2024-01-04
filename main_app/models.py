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

class Food(models.Model):
    name = models.CharField()
    calories = models.IntegerField()
    carbs = models.IntegerField()
    protein = models.IntegerField()
    amount = models.IntegerField(verbose_name='Weight(g)')
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('foods_update', kwargs={'food_id': self.id})

class Meal(models.Model):
    food = models.ManyToManyField(Food)
    servings = models.IntegerField()
    date = models.DateField(default=datetime.now)
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
    date = models.DateField(default=datetime.now)