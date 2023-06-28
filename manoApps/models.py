from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Car(models.Model):
    # saugom auto gamintoja
    make = models.CharField(max_length=100)

    def __str__(self):
        # grazina auto gamintoja kaip txt
        return self.make


class CarModel(models.Model):
    # jungtis su Car
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    # saugom auto modeli
    model = models.CharField(max_length=100)

    def __str__(self):
        # grazina auto modeli kaip txt
        return self.model


class UserCar(models.Model):
    # jungtis su User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # jungtis su CarModel
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    # auto metai, sveikasis sk.
    car_year = models.IntegerField()
    # auto degalai, txt max 50
    fuel_type = models.CharField(max_length=50)
    # auto rida, sveikasis, defaultine 0, nenaudojamas
    odometer_value = models.IntegerField(default=0)
    # auto nuvaziuotas astumas, defaultine 0, nenaudojamas
    driven_distance = models.IntegerField(default=0)
    # auto degalu kiekis bake, su kableliu, defaultine 0, nenaudojamas
    fuel_in_tank = models.FloatField(default=0)
    # auto vin kodas, min 17 / max 20, unikalus, defaultine 0
    VIN = models.CharField(max_length=20, unique=True, default=0, validators=[MinLengthValidator(17)])
    # auto numeriai, max 10, unikalus
    car_plate = models.CharField(max_length=10, unique=True)

    def __str__(self):
        # grazina auto modeli ir numerius kaip txt
        return f'{self.car_model.model} - {self.car_plate}'


class GasStationName(models.Model):
    # degalines imones pavadinimas, max 100, unikalus
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # grazina imones pavadinima kaip txt
        return self.name


class GasStation(models.Model):
    # saugom degalines pavadinima, max 100
    name = models.CharField(max_length=100)
    # degalines vieta, max 200
    location = models.CharField(max_length=200)
    # jungtis su UserCar
    user_car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    # data
    date = models.DateField()
    # saugoti degalų kainą max 5, po kablelio 3, defaultine 0, nenaudojamas
    price = models.DecimalField(default=0, max_digits=5, decimal_places=3)

    def __str__(self):
        # grazina degalines pavadinima kaip txt
        return self.name


class CarMileage(models.Model):
    # jungtis su UserCar
    user_car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    # jungtis su GasStation
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    # auto rida, sveikasis, defaultine 0
    odometer_value = models.IntegerField(default=0)
    # auto degalu kiekis bake, su kableliu, defaultine 0
    fuel_in_tank = models.FloatField(default=0)
    # auto nuvaziuotas astumas, defaultine 0
    driven_distance = models.IntegerField(default=0)
    # saugoti degalų kainą max 5, po kablelio 3, defaultine 0
    price = models.DecimalField(max_digits=5, decimal_places=3)
    # fiksuojam laika kai naujas irasas automatiskai
    timestamp = models.DateTimeField(auto_now_add=True)


class CarServiceEvent(models.Model):
    # jungtis su User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # jungtis su UserCar
    car = models.ForeignKey(UserCar, on_delete=models.CASCADE)
    # pavadinimas max 100
    name = models.CharField(max_length=100)
    # data
    date = models.DateField()
    # aprasymas txt
    description = models.TextField()
    # kaina max 5, po kablelio 2, defaultine 0
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)