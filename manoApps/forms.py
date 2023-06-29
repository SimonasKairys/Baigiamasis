from django import forms
from django.core.validators import MinLengthValidator
from .models import Car, CarModel, UserCar, GasStation, GasStationName, CarServiceEvent, CarMileage
from django.core.exceptions import ValidationError
from datetime import datetime


class GasStationNameSelectWidget(forms.Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['data-custom'] = 'custom'
        return option


class UserCarForm(forms.ModelForm):
    # formoje papildomai sukuriam driven_distance, defaultine reiksme 0
    driven_distance = forms.IntegerField(required=False, initial=0)

    class Meta:
        # nurodom formos modeli UserCar
        model = UserCar
        #  nurodom laukus kurie turi buti formoje
        fields = ('car_model', 'car_year', 'fuel_type', 'VIN', 'car_plate')


class CarMileageForm(forms.ModelForm):
    class Meta:
        # nurodom formos modeli CarMileage
        model = CarMileage
        #  nurodom laukus kurie turi buti formoje
        fields = ['odometer_value', 'fuel_in_tank', 'driven_distance', 'price']


class AddCarForm(forms.Form):
    # laukas 'car' kuris leidzia pasirinkti objekta is Car modeliu saraso
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    # laukas 'car_model' kuris neturi jokiu CarModel objektų, taciau atsinaujina
    car_model = forms.ModelChoiceField(queryset=CarModel.objects.none())
    # laukas 'car_year' sveikasis skaicius
    current_year = datetime.now().year
    car_year = forms.IntegerField(min_value=1900, max_value=current_year)
    # laukas 'VIN' ne maziau 17 ir ne daugiau 20 simboliu
    VIN = forms.CharField(max_length=20, validators=[MinLengthValidator(17)])
    # laukas 'car_plate' ne daugiau 10 simboliu
    car_plate = forms.CharField(max_length=10)
    # laukas 'fuel_type' leidzia rinktis tipa is saraso
    fuel_type = forms.ChoiceField(choices=[('gasoline', 'Gasoline'), ('diesel', 'Diesel')])
    # laukas 'odometer_value' sveikasis skaicius
    odometer_value = forms.IntegerField()
    # laukas 'driven_distance' sveikasis skaicius
    driven_distance = forms.IntegerField()
    # laukas 'fuel_in_tank' skaicius su kableliu
    fuel_in_tank = forms.FloatField()
    # laukas 'gas_station_name' pasirenkamas is GasStationName modelio saraso
    gas_station_name = forms.ModelChoiceField(
        queryset=GasStationName.objects.all(), required=True, label='Gas Station Name')
    # laukas 'gas_station_location' degalines vieta, privaloma
    gas_station_location = forms.CharField(required=True, label='Gas Station Location')
    # laukas 'price' viso max 5 skaiciai, po kablelio max 3
    price = forms.DecimalField(max_digits=5, decimal_places=3)
    # Laukas 'date' skirtas ivesti datai
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'format': 'YYYY-MM-DD',
                'endDate': '+0d'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tikrinam ar 'car' yra duomenyse
        if 'car' in self.data:
            try:
                car_id = int(self.data.get('car'))
                # filtruojam 'car_model' pagal 'car_id'
                self.fields['car_model'].queryset = CarModel.objects.filter(car_id=car_id)
            except (ValueError, TypeError):
                pass
            # Tikrinam ar 'car' yra
        elif self.initial.get('car') is not None:
            # filtruojam 'car_model' pagal 'car'
            self.fields['car_model'].queryset = CarModel.objects.filter(car=self.initial.get('car'))

    def clean_VIN(self):
        # gaunam 'VIN' reiksme
        VIN = self.cleaned_data.get('VIN')
        if UserCar.objects.filter(VIN=VIN).exists():
            # Tikrinam ar kitas UserCar yra su tokiu VIN
            user = UserCar.objects.get(VIN=VIN).user.username
            # grazinam userio varda
            raise ValidationError(f"This VIN is already used by {user}")
        return VIN

    def clean_car_plate(self):
        # gaunam 'car_plate' reiksme
        car_plate = self.cleaned_data.get('car_plate')
        if UserCar.objects.filter(car_plate=car_plate).exists():
            # Tikrinam ar kitas UserCar yra su tokiu car_plate
            user = UserCar.objects.get(car_plate=car_plate).user.username
            # grazinam userio varda
            raise ValidationError(f"This car_plate is already used by {user}")
        return car_plate


class EditCarForm(forms.ModelForm):
    class Meta:
        # nurodom formos modeli UserCar
        model = UserCar
        #  nurodom laukus kurie turi buti formoje
        fields = ['car_model', 'car_year']
    # sukuriam paildomus laukus driven_distance ir fuel_in_tank
    driven_distance = forms.IntegerField()
    fuel_in_tank = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        # kintamajam carmileage_id priskiriam kvargs 'carmileage_id' reiksme
        carmileage_id = kwargs.pop('carmileage_id', None)
        super().__init__(*args, **kwargs)

        if carmileage_id:
            # Gaunam CarMileage pagal carmileage_id
            car_mileage = CarMileage.objects.get(id=carmileage_id)
            # Nustatom pradines reiksmes 'driven_distance', 'fuel_in_tank' laukams is CarMileage
            self.fields['driven_distance'].initial = car_mileage.driven_distance
            self.fields['fuel_in_tank'].initial = car_mileage.fuel_in_tank


class EditGasStationForm(forms.ModelForm):
    class Meta:
        # nurodom formos modeli GasStation
        model = GasStation
        #  nurodom laukus kurie turi buti formoje
        fields = ['name', 'location', 'date']

    # sukuriam paildoma lauka price max 5, po kablelio 3
    price = forms.DecimalField(max_digits=5, decimal_places=3)

    def __init__(self, *args, **kwargs):
        # kintamajam carmileage_id priskiriam kvargs 'carmileage_id' reiksme
        carmileage_id = kwargs.pop('carmileage_id', None)
        super().__init__(*args, **kwargs)

        if carmileage_id:
            # Gaunam CarMileage pagal carmileage_id.
            car_mileage = CarMileage.objects.get(id=carmileage_id)
            # Nustatom pradine reiksme is CarMileage
            self.fields['price'].initial = car_mileage.price


class AddMileageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # kintamajam self.user priskiriam kvargs 'user' ir 'user_car_id' reiksme
        self.user = kwargs.pop('user', None)
        self.user_car_id = kwargs.pop('user_car_id', None)
        super().__init__(*args, **kwargs)
        # filtruojam 'CarMileage' pagal 'user_car_id' ir gaunam paskutini 'odometer_value' arba none
        last_car_mileage = CarMileage.objects.filter(user_car_id=self.user_car_id).order_by('-id').first()
        last_odometer_value = last_car_mileage.odometer_value if last_car_mileage else None

        # Sukuriam last_odometer_value ir jam nustatom pradinie odometer_value reiksme
        self.fields['last_odometer_value'] = forms.IntegerField(
            label="Last Odometer Value",
            initial=last_odometer_value,
            required=False,
            widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background-color: #f0f0f0;'}))

    # formos laukai
    odometer_value = forms.IntegerField(label='Odometer Value')
    fuel_in_tank = forms.IntegerField(label='Fuel in Tank')
    gas_station_name = forms.ModelChoiceField(
        queryset=GasStationName.objects.all(), required=True, label='Gas Station Name')
    gas_station_location = forms.CharField(label='Gas Station Location', max_length=100)
    price = forms.DecimalField(label='Price EUR', max_digits=5, decimal_places=3)
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'format': 'yyyy-mm-dd'
            }
        )
    )

    def clean(self):
        # isvalom laukus
        cleaned_data = super().clean()
        # gaunam isvalytus duomenis pagal laukus
        odometer_value = cleaned_data.get('odometer_value')
        fuel_in_tank = cleaned_data.get('fuel_in_tank')
        car_year = cleaned_data.get('car_year')
        price = cleaned_data.get('price')
        # Tikrinam ar odometer_value neigiamas arba lygus nuliui
        if odometer_value is not None and odometer_value <= 0:
            self.add_error('odometer_value', ValidationError('Odometer value must be greater than 0.'))
        # Tikrinam ar fuel_in_tank neigiamas
        if fuel_in_tank is not None and fuel_in_tank < 0:
            self.add_error('fuel_in_tank', ValidationError('Fuel in tank must be non-negative.'))
        # Tikrinam ar car_year neigiamas
        if car_year is not None and car_year < 0:
            self.add_error('car_year', ValidationError('Car year must be non-negative.'))
        # Tikrinam ar price neigiamas
        if price is not None and price < 0:
            self.add_error('price', ValidationError('Price must be non-negative.'))
        # Gaunam paskutine CarMileage odometer_value reiksme arba nustatytom 0 jei neegzistuoja.
        last_car_mileage = CarMileage.objects.filter(user_car_id=self.user_car_id).order_by('-id').first()
        last_odometer_value = last_car_mileage.odometer_value if last_car_mileage else 0
        # Tikrinam ar odometer_value mažesnis arba lygus paskutiniai vertei
        if odometer_value is not None and odometer_value <= last_odometer_value:
            self.add_error('odometer_value',
                           ValidationError('Odometer value must be greater than the last saved value.'))

        return cleaned_data


class CarServiceEventForm(forms.ModelForm):
    # Sukuriam 'date' lauka
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'format': 'YYYY-MM-DD'
            }
        )
    )

    class Meta:
        # nurodom formos modeli CarServiceEvent
        model = CarServiceEvent
        #  nurodom laukus kurie turi buti formoje
        fields = ['car', 'name', 'date', 'description', 'price']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # grazina 'car' susijusius su konkreciu useriu
        self.fields['car'].queryset = self.get_user_cars(user)

    def get_user_cars(self, user):
        # Gaunam userio auto iš UserCar
        return UserCar.objects.filter(user=user)

