from django import forms
from .models import Car, CarModel, UserCar, GasStation


class AddCarForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.none())
    car_year = forms.IntegerField()
    fuel_type = forms.ChoiceField(choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel')])
    odometer_value = forms.IntegerField()
    fuel_in_tank = forms.FloatField()
    gas_station_name = forms.CharField(required=True, label='Gas Station Name')
    gas_station_location = forms.CharField(required=True, label='Gas Station Location')
    date = forms.DateField()
    price = forms.DecimalField(max_digits=5, decimal_places=3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'car' in self.data:
            try:
                car_id = int(self.data.get('car'))
                self.fields['car_model'].queryset = CarModel.objects.filter(car_id=car_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get('car') is not None:
            self.fields['car_model'].queryset = CarModel.objects.filter(car=self.initial.get('car'))


class EditCarForm(forms.ModelForm):
    class Meta:
        model = UserCar
        fields = [
            'car_model',
            'car_year',
            'fuel_type',
            'odometer_value',
            'fuel_in_tank',
        ]


class EditGasStationForm(forms.ModelForm):
    class Meta:
        model = GasStation
        fields = [
            'name',
            'location',
            'date',
            'price'
        ]


class AddMileageForm(forms.Form):
    odometer_value = forms.IntegerField(label='Odometer Value')
    fuel_in_tank = forms.IntegerField(label='Fuel in Tank')
    gas_station_name = forms.CharField(label='Gas Station Name', max_length=100)
    gas_station_location = forms.CharField(label='Gas Station Location', max_length=100)
    date = forms.DateField()
    price = forms.DecimalField(label='Price EUR', max_digits=5, decimal_places=3)
