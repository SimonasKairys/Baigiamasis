from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


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
    odometer_value = models.IntegerField(default=0)
    driven_distance = models.IntegerField(default=0)
    fuel_in_tank = models.FloatField(default=0)
    VIN = models.CharField(max_length=20, unique=True, default=0, validators=[MinLengthValidator(17)])
    car_plate = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.car_model.model} - {self.car_plate}'


class GasStationName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class GasStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    user_car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=3)

    def __str__(self):
        return self.name


class CarMileage(models.Model):
    user_car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    odometer_value = models.IntegerField()
    fuel_in_tank = models.FloatField()
    driven_distance = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    timestamp = models.DateTimeField(auto_now_add=True)


class CarServiceEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)