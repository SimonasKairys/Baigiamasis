from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserCar, GasStation, GasStationName, CarServiceEvent, CarModel, CarMileage
from .forms import AddCarForm, EditCarForm, EditGasStationForm, AddMileageForm, CarServiceEventForm
from datetime import date
from django.db.models import Sum, F, FloatField
from django.contrib import messages


def home_page(request):
    """
     function for displaying home page

    :param request: HTTP request
    :return: renders object
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    car_id = request.GET.get('car_id', None)
    user_cars = UserCar.objects.filter(user=request.user).distinct()

    unique_cars_data = []

    for user_car in user_cars:
        car_mileages = CarMileage.objects.filter(user_car=user_car)
        if car_mileages:
            aggregated_data = car_mileages.aggregate(
                total_driven_distance=Sum('driven_distance'),
                total_fuel=Sum('fuel_in_tank'),
                total_price=Sum(F('fuel_in_tank') * F('price'), output_field=FloatField())
            )

            average_fuel_consumption = (aggregated_data['total_fuel'] / aggregated_data['total_driven_distance']) * 100\
                if aggregated_data['total_fuel'] and aggregated_data['total_driven_distance'] else 0
            average_fuel_consumption = "{:.3f}".format(average_fuel_consumption)

            car_make = user_car.car_model.car.make
            car_model = user_car.car_model.model
            car_plate = user_car.car_plate

            total_service_price = \
                CarServiceEvent.objects.filter(car=user_car).aggregate(total_service_price=Sum('price')
                                                                       )['total_service_price']
            total_service_price = total_service_price if total_service_price else 0

            unique_cars_data.append({
                'user_car_id': user_car.id,
                'car_make': car_make,
                'car_model': car_model,
                'car_plate': car_plate,
                'total_driven_distance': aggregated_data['total_driven_distance'],
                'total_fuel': aggregated_data['total_fuel'],
                'total_price': aggregated_data['total_price'],
                'average_fuel_consumption': average_fuel_consumption,
                'total_service_price': total_service_price,
            })

    context = {
        'user': request.user,
        'user_cars': user_cars,
        'car_id': car_id,
        'unique_cars_data': unique_cars_data,
    }
    return render(request, 'manoApps/logged_home.html', context)


def register(request):
    """
     user registration

    :param request: HTTP request
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'manoApps/register.html', {'form': form})


def user_login(request):
    """
    user login

    :param request: HTTP request
    :return: return to login page
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Index')
    else:
        form = AuthenticationForm()
    return render(request, 'manoApps/login.html', {'form': form})


def user_logout(request):
    """
    user logout

    :param request: HTTP request
    :return: return to login page
    """
    logout(request)
    return redirect('login')


def logged_home(request):
    """
    returns to home page after login

    :param request: HTTP request
    :return: home page after login
    """
    return render(request, 'manoApps/logged_home.html')


@login_required
def add_car(request):
    """
     function for adding a new car

    :param request: HTTP request
    :return: render object
    """
    request.GET.get('car') if request.method == 'GET' else None

    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            user_car = UserCar(
                user=request.user,
                car_model=form.cleaned_data['car_model'],
                car_year=form.cleaned_data['car_year'],
                fuel_type=form.cleaned_data['fuel_type'],
                VIN=form.cleaned_data['VIN'],
                car_plate=form.cleaned_data['car_plate'],
            )
            user_car.save()

            gas_station_name = form.cleaned_data['gas_station_name']

            if not isinstance(gas_station_name, GasStationName):
                new_gas_station_name = GasStationName(name=gas_station_name)
                new_gas_station_name.save()
            else:
                new_gas_station_name = gas_station_name

            gas_station = GasStation(
                name=new_gas_station_name.name,
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                user_car=user_car
            )

            gas_station.save()

            car_mileage = CarMileage(
                user_car=user_car,
                gas_station=gas_station,
                odometer_value=form.cleaned_data['odometer_value'],
                fuel_in_tank=form.cleaned_data['fuel_in_tank'],
                driven_distance=form.cleaned_data['driven_distance'],
                price=form.cleaned_data['price'],
            )
            car_mileage.save()
            return redirect('your_car_info')
        else:
            messages.error(request, form.errors)
    else:
        form = AddCarForm()
    return render(request, 'manoApps/add_car.html', {'form': form})


@login_required
def your_car_info(request):
    """
    displays the user's registered cars info

    :param request: HTTP request
    :return: displays car info
    """
    user_cars = UserCar.objects.filter(user=request.user)
    return render(request, 'manoApps/your_car_info.html', {'user_cars': user_cars})


@login_required
def edit_car(request, car_id, carmileage_id):
    """
    function for editing existing car

    :param request: HTTP request
    :param car_id: id of the car being edited
    :param carmileage_id: id of the edited car in the carmileage table
    :return: render object
    """
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    gas_station = GasStation.objects.filter(user_car=user_car).first()
    car_mileage = CarMileage.objects.get(id=carmileage_id)

    if request.method == 'POST':
        form_car = EditCarForm(request.POST, instance=user_car)
        form_gas_station = EditGasStationForm(request.POST, instance=gas_station)

        if form_car.is_valid() and form_gas_station.is_valid():
            form_car.save()
            form_gas_station.save()

            car_mileage.driven_distance = form_car.cleaned_data['driven_distance']
            car_mileage.fuel_in_tank = form_car.cleaned_data['fuel_in_tank']
            car_mileage.price = form_gas_station.cleaned_data['price']
            car_mileage.save()
            return redirect('your_car_info')
    else:
        initial_car_data = {
            'driven_distance': car_mileage.driven_distance,
            'fuel_in_tank': car_mileage.fuel_in_tank
        }
        initial_gas_station_data = {
            'price': car_mileage.price
        }
        form_car = EditCarForm(instance=user_car, initial=initial_car_data)
        form_gas_station = EditGasStationForm(instance=gas_station, initial=initial_gas_station_data)

    context = {
        'form_car': form_car,
        'form_gas_station': form_gas_station,
        'carmileage_id': carmileage_id
    }
    return render(request, 'manoApps/edit_car.html', context)


@login_required
def delete_car(request, car_id, gas_station_id):
    """
    function for deleting existing car

    :param request: HTTP request
    :param car_id: car id which is removed
    :param gas_station_id: gas station id which is removed
    :return: render object
    """
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    gas_station = get_object_or_404(GasStation, id=gas_station_id, user_car=user_car)

    initial_count = user_car.gasstation_set.count()

    gas_station.delete()

    final_count = user_car.gasstation_set.count()

    if initial_count == 1 and final_count == 0:
        user_car.delete()
    return redirect('your_car_info')


@login_required
def add_mileage(request, user_car_id):
    """
    function for updating car's mileage

    :param request: HTTP request
    :param user_car_id: user's car id
    :return: renders object
    """
    original_user_car = get_object_or_404(UserCar, id=user_car_id)
    initial_data = {'date': date.today()}

    if request.method == 'POST':
        form = AddMileageForm(request.POST, user=request.user, user_car_id=user_car_id)

        if form.is_valid():
            new_odometer_value = form.cleaned_data['odometer_value']
            last_car_mileage = CarMileage.objects.filter(user_car_id=user_car_id).order_by('-id').first()
            last_odometer_value = last_car_mileage.odometer_value if last_car_mileage else 0

            driven_distance = new_odometer_value - last_odometer_value

            gas_station_name = form.cleaned_data['gas_station_name']

            if not isinstance(gas_station_name, GasStationName):
                new_gas_station_name = GasStationName(name=gas_station_name)
                new_gas_station_name.save()
            else:
                new_gas_station_name = gas_station_name

            gas_station = GasStation(
                name=new_gas_station_name.name,
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                user_car=original_user_car,
            )
            gas_station.save()

            car_mileage = CarMileage(
                user_car=original_user_car,
                gas_station=gas_station,
                odometer_value=new_odometer_value,
                fuel_in_tank=form.cleaned_data['fuel_in_tank'],
                driven_distance=driven_distance,
                price=form.cleaned_data['price'],
            )
            car_mileage.save()

            return redirect('your_car_info')
    else:
        form = AddMileageForm(initial=initial_data, user=request.user, user_car_id=user_car_id)

    return render(request, 'manoApps/add_mileage.html', {'form': form, 'user_car': original_user_car})


@login_required
def info_service(request):
    """
    function shows repairs of car

    :param request: HTTP request
    :return: render object
    """
    services = CarServiceEvent.objects.filter(user=request.user)
    return render(request, 'manoApps/info_service.html', {'services': services})


@login_required
def service_new(request):
    """
    function for new car repair registration

    :param request: HTTP request
    :return: render object
    """
    user_cars = CarModel.objects.filter(usercar__user=request.user).values_list('id', flat=True).distinct()
    if user_cars.count() == 0:
        return redirect('add_car')

    if request.method == "POST":
        form = CarServiceEventForm(request.user, request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect('info_service')
    else:
        if user_cars.count() > 1:
            form = CarServiceEventForm(request.user)
        elif user_cars.count() == 1:
            form = CarServiceEventForm(request.user, initial={'car': user_cars.first()})

    return render(request, 'manoApps/service_new.html', {'form': form})


@login_required
def service_edit(request, service_id):
    """
    function for update car repair's

    :param request: HTTP request
    :param service_id: repair id
    :return: renders object
    """
    service = get_object_or_404(CarServiceEvent, id=service_id)
    if request.method == 'POST':
        form = CarServiceEventForm(request.user, request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('info_service')
    else:
        form = CarServiceEventForm(request.user, instance=service)

    return render(request, 'manoApps/service_edit.html', {'form': form})


@login_required
def service_delete(request, service_id):
    """
    function for deleting existing car repair

    :param service_id: repair id
    :return: renders object
    """
    service = get_object_or_404(CarServiceEvent, id=service_id)
    service.delete()
    return redirect('info_service')


def about(request):
    """
    :param request: HTTP request
    :return: renders object
    """
    return render(request, 'manoApps/about.html')


def contacts(request):
    """
    :param request: HTTP request
    :return: renders object
    """
    return render(request, 'manoApps/contacts.html')

