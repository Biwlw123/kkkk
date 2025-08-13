from django.db import models
from django.contrib.auth import get_user_model
import os
from urllib.parse import urlparse
from io import BytesIO
import requests
from django.core.files import File


class Car(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='owner')
    vin = models.CharField(max_length=17, null=True)
    number = models.CharField(max_length=9, null=True)
    color = models.CharField(max_length=20, null=True)
    release_year = models.CharField(max_length=4, null=True)
    brand = models.CharField(max_length=20, null=True)
    current_mileage = models.IntegerField(null=True)
    last_inspection_mileage = models.IntegerField(null=True)
    daily_mileage = models.IntegerField(null=True)
    usage_conditions = models.CharField(
        max_length=10,
        choices=(
           ('city', 'Город'),
           ('highway', 'Шоссе'),
           ('off-road', 'Бездорожье'),
           ('mixed', 'Смешанный'),
        ),
        null=True
    )
    driving_style = models.CharField(
        max_length=13,
        choices=(
           ('calm', 'Спокойный'),
           ('universal', 'Универсальный'),
           ('agressive', 'Агрессивный'),
        ),
        null=True
    )
    usage_type = models.CharField(
        max_length=8,
        choices=(
           ('personal', 'Личный'),
           ('taxi', 'Такси'),
           ('rental', 'Прокат'),
           ('delivery', 'Доставка'),
        ),
        null=True
    )
    oil = models.IntegerField(null=True)
    oil_filter = models.IntegerField(null=True)
    belt = models.IntegerField(null=True)
    transmission = models.IntegerField(null=True)
    air_filter = models.IntegerField(null=True)
    cabin_filter = models.IntegerField(null=True)
    fuel_filter = models.IntegerField(null=True)
    coolant = models.IntegerField(null=True)
    spark_plugs = models.IntegerField(null=True)
    brake_fluid = models.IntegerField(null=True)
    brakes = models.IntegerField(null=True)
    shocks = models.IntegerField(null=True)
    steering = models.IntegerField(null=True)
    battery = models.IntegerField(null=True)
    tires = models.IntegerField(null=True)
    quiz_date = models.DateTimeField(null=True)
    last_inspection_date = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='cars/', default='cars/default_car.png', null=True)
