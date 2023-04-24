from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserCar, GasStation
from .forms import AddCarForm, EditCarForm, EditGasStationForm, AddMileageForm
from datetime import date


def home_page(request):
    return render(request, 'manoApps/mano_home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'manoApps/mano_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('logged_home')
    else:
        form = AuthenticationForm()
    return render(request, 'manoApps/mano_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def logged_home(request):
    return render(request, 'manoApps/mano_home.html')


@login_required
def add_car(request):
    car_id = request.GET.get('car') if request.method == 'GET' else None

    initial_data = {'date': date.today()}
    if car_id is not None:
        initial_data['car'] = car_id
    form = AddCarForm(initial=initial_data)

    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            user_car = UserCar(
                user=request.user,
                car_model=form.cleaned_data['car_model'],
                car_year=form.cleaned_data['car_year'],
                fuel_type=form.cleaned_data['fuel_type'],
                odometer_value=form.cleaned_data['odometer_value'],
                fuel_in_tank=form.cleaned_data['fuel_in_tank']
            )
            user_car.save()

            gas_station = GasStation(
                name=form.cleaned_data['gas_station_name'],
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                price=form.cleaned_data['price'],
                user_car=user_car
            )
            gas_station.save()

            return redirect('your_car_info')

    return render(request, 'manoApps/add_car.html', {'form': form})


def your_car_info(request):
    user_cars = UserCar.objects.filter(user=request.user)
    return render(request, 'manoApps/your_car_info.html', {'user_cars': user_cars})


@login_required
def edit_car(request, car_id):
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    gas_station = get_object_or_404(GasStation, user_car=user_car)

    if request.method == 'POST':
        form_car = EditCarForm(request.POST, instance=user_car)
        form_gas_station = EditGasStationForm(request.POST, instance=gas_station)

        if form_car.is_valid() and form_gas_station.is_valid():
            form_car.save()
            form_gas_station.save()
            return redirect('your_car_info')
    else:
        form_car = EditCarForm(instance=user_car)
        form_gas_station = EditGasStationForm(instance=gas_station, initial={'date': date.today()})

    return render(request, 'manoApps/edit_car.html', {'form_car': form_car, 'form_gas_station': form_gas_station})


@login_required
def delete_car(request, car_id):
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    gas_station = get_object_or_404(GasStation, user_car=user_car)

    gas_station.delete()
    user_car.delete()

    return redirect('your_car_info')


@login_required
def add_mileage(request, user_car_id):
    original_user_car = get_object_or_404(UserCar, id=user_car_id)
    initial_data = {'date': date.today()}
    if request.method == 'POST':
        form = AddMileageForm(request.POST)
        if form.is_valid():
            new_user_car = UserCar(
                user=request.user,
                car_model=original_user_car.car_model,
                car_year=original_user_car.car_year,
                fuel_type=original_user_car.fuel_type,
                odometer_value=form.cleaned_data['odometer_value'],
                fuel_in_tank=form.cleaned_data['fuel_in_tank']
            )
            new_user_car.save()

            gas_station = GasStation(
                user_car=new_user_car,
                name=form.cleaned_data['gas_station_name'],
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                price=form.cleaned_data['price']
            )
            gas_station.save()

            return redirect('your_car_info')
    else:
        form = AddMileageForm(initial=initial_data)

    return render(request, 'manoApps/add_mileage.html', {'form': form, 'user_car': original_user_car})

