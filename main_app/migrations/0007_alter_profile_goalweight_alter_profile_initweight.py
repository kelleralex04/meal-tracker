# Generated by Django 5.0 on 2024-01-04 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_food_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='goalWeight',
            field=models.IntegerField(verbose_name='Goal Weight'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='initWeight',
            field=models.IntegerField(verbose_name='Staring Weight'),
        ),
    ]