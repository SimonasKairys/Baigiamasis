from django import forms
from .models import Car, CarModel, UserCar, GasStation


class AddCarForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    # car_model = forms.ModelChoiceField(queryset=CarModel.objects.none(), required=True, label='Car Model')
    # car_model = forms.ModelChoiceField(queryset=CarModel.objects.none())
    car_model = forms.CharField()
    car_year = forms.IntegerField()
    fuel_type = forms.ChoiceField(choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel')])
    odometer_value = forms.IntegerField()
    fuel_in_tank = forms.FloatField()
    gas_station_name = forms.CharField(required=True, label='Gas Station Name')
    gas_station_location = forms.CharField(required=True, label='Gas Station Location')
    date = forms.DateField()
    price = forms.DecimalField(max_digits=10, decimal_places=3)

    def __init__(self, *args, **kwargs):
        car_id = kwargs.pop('car_id', None)
        super().__init__(*args, **kwargs)

        if car_id:
            self.fields['car_model'].queryset = CarModel.objects.filter(car_id=car_id).order_by('model')


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
