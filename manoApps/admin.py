from django.contrib import admin
from .models import Car, CarModel, UserCar, GasStationName

# sukuriam klase CarAdmin (admin psl) ir nurodom kas bus rodoma Car modelyje
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make')

# sukuriam klase CarModelAdmin (admin psl) ir nurodom kas bus rodoma CarModel modelyje
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'model')

# sukuriam klase UserCarAdmin (admin psl) ir nurodom kas bus rodoma UserCar modelyje
class UserCarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_model', 'car_year', 'fuel_type', 'odometer_value', 'fuel_in_tank')

# sukuriam klase GasStationNameAdmin (admin psl) ir nurodom kas bus rodoma GasStationName modelyje
class GasStationNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

# sukuriami modeliai su virsuje nurodytais nuostatais
admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(UserCar, UserCarAdmin)
admin.site.register(GasStationName, GasStationNameAdmin)
