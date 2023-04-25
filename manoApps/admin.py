from django.contrib import admin
from .models import Car, CarModel, UserCar, GasStationName


# @admin.action(description='make public')
# def make_published(queryset):
#     queryset.update(genre='Adventure')


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'model')


class UserCarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_model', 'car_year', 'fuel_type', 'odometer_value', 'fuel_in_tank')


class GasStationNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(UserCar, UserCarAdmin)
admin.site.register(GasStationName, GasStationNameAdmin)
