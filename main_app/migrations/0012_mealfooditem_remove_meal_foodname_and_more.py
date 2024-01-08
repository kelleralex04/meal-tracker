# Generated by Django 5.0 on 2024-01-06 00:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_remove_meal_food_meal_foodname'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealFoodItem',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main_app.food')),
                ('servings', models.IntegerField()),
            ],
            bases=('main_app.food',),
        ),
        migrations.RemoveField(
            model_name='meal',
            name='foodname',
        ),
        migrations.RemoveField(
            model_name='meal',
            name='servings',
        ),
        migrations.AddField(
            model_name='meal',
            name='food',
            field=models.ManyToManyField(to='main_app.mealfooditem'),
        ),
    ]