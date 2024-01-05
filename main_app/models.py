from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.postgres.fields import ArrayField

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
    foodname = ArrayField(models.CharField())
    servings = models.IntegerField()
    date = models.DateField(default=datetime.now)
    favorited = models.BooleanField(default=False)
    mealType = models.CharField(
        max_length=1,
        choices=MEALCHOICE,
        default=MEALCHOICE[0][0]
    )

class Profile(models.Model):
    firstname = models.CharField(verbose_name = 'First Name')
    lastname = models.CharField(verbose_name = 'Last Name')
    age = models.IntegerField()
    height = models.IntegerField(verbose_name = 'Height(cm)')
    initWeight = models.IntegerField(verbose_name='Staring Weight')
    goalWeight = models.IntegerField(verbose_name='Goal Weight')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.id})


class BodyData(models.Model):
    weight = models.IntegerField()
    date = models.DateField(default=datetime.now)