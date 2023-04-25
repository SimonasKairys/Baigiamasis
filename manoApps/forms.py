from django import forms
from .models import Car, CarModel, UserCar, GasStation, GasStationName
from django.core.exceptions import ValidationError


class GasStationNameSelectWidget(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['data-custom'] = 'custom'
        return option


class AddCarForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.none())
    car_year = forms.IntegerField()
    fuel_type = forms.ChoiceField(choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel')])
    odometer_value = forms.IntegerField()
    fuel_in_tank = forms.FloatField()
    gas_station_name = forms.ModelChoiceField(
        queryset=GasStationName.objects.all(), required=True, label='Gas Station Name',
        widget=GasStationNameSelectWidget(attrs={'data-allow-custom': 'true'}))
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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.user_car_id = kwargs.pop('user_car_id', None)
        super().__init__(*args, **kwargs)
        last_user_car = UserCar.objects.filter(user=self.user, id=self.user_car_id).last()
        last_odometer_value = last_user_car.odometer_value if last_user_car else None

        self.fields['last_odometer_value'] = forms.IntegerField(
            label="Last Odometer Value",
            initial=last_odometer_value,
            required=False,
            widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: #f0f0f0;'}))

    odometer_value = forms.IntegerField(label='Odometer Value')
    fuel_in_tank = forms.IntegerField(label='Fuel in Tank')
    gas_station_name = forms.CharField(label='Gas Station Name', max_length=100)
    gas_station_location = forms.CharField(label='Gas Station Location', max_length=100)
    date = forms.DateField()
    price = forms.DecimalField(label='Price EUR', max_digits=5, decimal_places=3)

    def clean(self):
        cleaned_data = super().clean()
        odometer_value = cleaned_data.get('odometer_value')
        fuel_in_tank = cleaned_data.get('fuel_in_tank')
        car_year = cleaned_data.get('car_year')
        price = cleaned_data.get('price')

        if odometer_value is not None and odometer_value <= 0:
            self.add_error('odometer_value', ValidationError('Odometer value must be greater than 0.'))

        if fuel_in_tank is not None and fuel_in_tank < 0:
            self.add_error('fuel_in_tank', ValidationError('Fuel in tank must be non-negative.'))

        if car_year is not None and car_year < 0:
            self.add_error('car_year', ValidationError('Car year must be non-negative.'))

        if price is not None and price < 0:
            self.add_error('price', ValidationError('Price must be non-negative.'))

        user_car = UserCar.objects.filter(user=self.user, id=self.user_car_id).last()
        if user_car and odometer_value is not None and odometer_value <= user_car.odometer_value:
            self.add_error('odometer_value',
                           ValidationError('Odometer value must be greater than the last saved value.'))
