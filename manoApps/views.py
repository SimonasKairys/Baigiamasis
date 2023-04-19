from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserCar, GasStation
from .forms import AddCarForm, EditCarForm, EditGasStationForm


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
                user_car=user_car
            )
            gas_station.save()

            return redirect('your_car_info')
    else:
        form = AddCarForm()

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
        form_gas_station = EditGasStationForm(instance=gas_station)

    return render(request, 'manoApps/edit_car.html', {'form_car': form_car, 'form_gas_station': form_gas_station})


@login_required
def delete_car(request, car_id):
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    gas_station = get_object_or_404(GasStation, user_car=user_car)

    gas_station.delete()
    user_car.delete()

    return redirect('your_car_info')


