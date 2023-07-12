from django.contrib import admin
from .models import Car, CarModel, UserCar, GasStationName


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'model')


class UserCarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_model', 'car_year', 'fuel_type')


class GasStationNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(UserCar, UserCarAdmin)
admin.site.register(GasStationName, GasStationNameAdmin)
