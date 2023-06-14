from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    make = models.CharField(max_length=100)

    def __str__(self):
        return self.make


class CarModel(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.model


class UserCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    car_year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    odometer_value = models.IntegerField()
    driven_distance = models.IntegerField(default=0)
    fuel_in_tank = models.FloatField()
    VIN = models.CharField(max_length=20, unique=True, default=0)
    car_plate = models.CharField(max_length=10)

    def __str__(self):
        return self.car_model.model


class GasStationName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class GasStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    user_car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name


class CarServiceEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
