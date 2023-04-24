from django.contrib import admin
from .models import Asmenys, Car, CarModel, UserCar, GasStation


# @admin.action(description='make public')
# def make_published(queryset):
#     queryset.update(genre='Adventure')


class AsmenysAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_surname', 'user_birth_date', 'user_age']
    # ordering = ['user_name']
    # actions = [make_published]


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'model')


class UserCarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_model', 'car_year', 'fuel_type', 'odometer_value', 'fuel_in_tank')


class GasStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'user_car', 'date', 'price')


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(UserCar, UserCarAdmin)
admin.site.register(GasStation, GasStationAdmin)
admin.site.register(Asmenys, AsmenysAdmin)
