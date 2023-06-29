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
    # jeigu useris neprisijunges grazinam i login
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # gaunam car_id su get arba None jeigu nera
    car_id = request.GET.get('car_id', None)
    # istraukiam userio auto
    user_cars = UserCar.objects.filter(user=request.user).distinct()

    # sarasas kuriame saugosim unikalius auto
    unique_cars_data = []

    for user_car in user_cars:
        # gaunam auto rida
        car_mileages = CarMileage.objects.filter(user_car=user_car)
        if car_mileages:
            # auto modeli
            car_data = user_car.car_model

            # skaiciuojam duomenis is CarMileage lenteles pagal parametrus
            aggregated_data = car_mileages.aggregate(
                total_driven_distance=Sum('driven_distance'),
                total_fuel=Sum('fuel_in_tank'),
                total_price=Sum(F('fuel_in_tank') * F('price'), output_field=FloatField())
            )

            # skaiciuojam vidutines sanaudas
            average_fuel_consumption = (aggregated_data['total_fuel'] / aggregated_data['total_driven_distance']) * 100\
                if aggregated_data['total_fuel'] and aggregated_data['total_driven_distance'] else 0
            # apvalinam sanaudas iki 3 skaiciu po kablelio
            average_fuel_consumption = "{:.3f}".format(average_fuel_consumption)

            # auto gamintojas
            car_make = user_car.car_model.car.make
            # auto modelis
            car_model = user_car.car_model.model
            # auto numeriai
            car_plate = user_car.car_plate

            # serviso kaina
            total_service_price = \
                CarServiceEvent.objects.filter(car=user_car).aggregate(total_service_price=Sum('price')
                                                                       )['total_service_price']
            total_service_price = total_service_price if total_service_price is not None else 0

            # viska is virsaus sudedam cia
            unique_cars_data.append({
                'user_car_id': user_car.id,
                'car_make': car_make,
                'car_model': car_model,
                'car_data': car_data,
                'car_plate': car_plate,
                'car_mileages': car_mileages,
                'total_driven_distance': aggregated_data['total_driven_distance'],
                'total_fuel': aggregated_data['total_fuel'],
                'total_price': aggregated_data['total_price'],
                'average_fuel_consumption': average_fuel_consumption,
                'total_service_price': total_service_price,
            })
    # kas bus perduodama su context
    context = {
        'user': request.user,
        'user_cars': user_cars,
        'car_id': car_id,
        'unique_cars_data': unique_cars_data,
    }
    # grazinam visa info (context) i url
    return render(request, 'manoApps/mano_home.html', context)


def register(request):
    # tikrina ar POST tipas,
    if request.method == 'POST':
        # sukuria UserCreationForm naudojant ivestus duomenis
        form = UserCreationForm(request.POST)
        # tikrina ar geri duomenys
        if form.is_valid():
            # issaugo jei geri
            form.save()
            # nukreipia i login
            return redirect('login')
    else:
        # sukuria tuscia UserCreationForm
        form = UserCreationForm()
    # nukreipia i registracijos forma
    return render(request, 'manoApps/mano_register.html', {'form': form})


def user_login(request):
    # tikrina ar POST tipas,
    if request.method == 'POST':
        # sukuria AuthenticationForm naudojant ivestus duomenis
        form = AuthenticationForm(request, data=request.POST)
        # tikrina ar geri duomenys
        if form.is_valid():
            # tikrina ar teisingas username
            username = form.cleaned_data.get('username')
            # tikrina ar teisingas password
            password = form.cleaned_data.get('password')
            # autentifikacija
            user = authenticate(username=username, password=password)
            # jei sekminga
            if user is not None:
                # prijungia
                login(request, user)
                # prijungus nukreipia
                return redirect('Index')
    else:
        # sukuria tuscia AuthenticationForm
        form = AuthenticationForm()
    # nukreipia i ta forma
    return render(request, 'manoApps/mano_login.html', {'form': form})


def user_logout(request):
    # atjungia useri
    logout(request)
    # grazina i login url
    return redirect('login')


def logged_home(request):
    # atvaizduoja kaip pagrindini kai prisijunges useris
    return render(request, 'manoApps/mano_home.html')


@login_required  # tikrina ar prisijunges
def add_car(request):
    # gaunam car duomenis jeigu yra arba None
    request.GET.get('car') if request.method == 'GET' else None

    # tikrinam ar POST tipas,
    if request.method == 'POST':
        # jeigu POST sukuriam forma
        form = AddCarForm(request.POST)
        # jeigu forma ok
        if form.is_valid():
            # sukuriam UserCar su nurodytais laukais
            user_car = UserCar(
                user=request.user,
                car_model=form.cleaned_data['car_model'],
                car_year=form.cleaned_data['car_year'],
                fuel_type=form.cleaned_data['fuel_type'],
                VIN=form.cleaned_data['VIN'],
                car_plate=form.cleaned_data['car_plate'],
            )
            # issaugom db
            user_car.save()

            # priskiriam duomenis kuria buvo isvalyti ????
            gas_station_name = form.cleaned_data['gas_station_name']

            # tikrinam ar gas_station_name yra GasStationName
            if not isinstance(gas_station_name, GasStationName):
                # priskiriam nauja gas_station_name
                new_gas_station_name = GasStationName(name=gas_station_name)
                # issaugom db
                new_gas_station_name.save()
            else:
                # jeigu yra naudojam kas yra
                new_gas_station_name = gas_station_name

            # sukuriam GasStation su nurodytais laukais
            gas_station = GasStation(
                name=new_gas_station_name.name,
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                user_car=user_car
            )
            # issaugom db
            gas_station.save()

            # sukuriam CarMileage su nurodytais laukais
            car_mileage = CarMileage(
                user_car=user_car,
                gas_station=gas_station,
                odometer_value=form.cleaned_data['odometer_value'],
                fuel_in_tank=form.cleaned_data['fuel_in_tank'],
                driven_distance=form.cleaned_data['driven_distance'],
                price=form.cleaned_data['price'],
            )
            # issaugom db
            car_mileage.save()
            # jei viskas ok, nukreipiam i url
            return redirect('your_car_info')
        else:
            # errorai
            messages.error(request, form.errors)
    else:
        # tuscia forma
        form = AddCarForm()
    # nukreipiam i url su tuscia forma
    return render(request, 'manoApps/add_car.html', {'form': form})


@login_required  # tikrina ar prisijunges
def your_car_info(request):
    # gaunam visus userio auto
    user_cars = UserCar.objects.filter(user=request.user)
    # atvaizuodam url su duomenim
    return render(request, 'manoApps/your_car_info.html', {'user_cars': user_cars})


@login_required  # tikrina ar prisijunges
def edit_car(request, car_id, carmileage_id):
    # gaunam UserCar pagal car_id ir prisijungusi useri
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    # gaunam GasStation pagal user_car
    gas_station = GasStation.objects.filter(user_car=user_car).first()
    # gaunam CarMileage pagal carmileage_id
    car_mileage = CarMileage.objects.get(id=carmileage_id)

    # tikrinam ar POST uzklausa
    if request.method == 'POST':
        # sukuriam EditCarForm naudojant POST duomenis pagal user_car
        form_car = EditCarForm(request.POST, instance=user_car)
        # sukuriam EditGasStationForm naudojant POST duomenis pagal gas_station
        form_gas_station = EditGasStationForm(request.POST, instance=gas_station)

        # tikrinam formas
        if form_car.is_valid() and form_gas_station.is_valid():
            # issaugom form_car (EditCarForm)
            form_car.save()
            # issaugom form_gas_station (EditGasStationForm)
            form_gas_station.save()

            # atnaujinam car_mileage driven_distance reiksme is form_car
            car_mileage.driven_distance = form_car.cleaned_data['driven_distance']
            # atnaujinam car_mileage fuel_in_tank reiksme is form_car
            car_mileage.fuel_in_tank = form_car.cleaned_data['fuel_in_tank']
            # atnaujinam car_mileage price reiksme is form_gas_station
            car_mileage.price = form_gas_station.cleaned_data['price']
            # issaugom i db
            car_mileage.save()
            # nukreipiam i url
            return redirect('your_car_info')
    else:
        initial_car_data = {
            # pradine driven_distance reiksme
            'driven_distance': car_mileage.driven_distance,
            # pradine fuel_in_tank reiksme
            'fuel_in_tank': car_mileage.fuel_in_tank
        }
        initial_gas_station_data = {
            # pradine price reiksme
            'price': car_mileage.price
        }
        # sukuriam EditCarForm naudojant user_car ir pradinius duomenis
        form_car = EditCarForm(instance=user_car, initial=initial_car_data)
        # sukuriam EditGasStationForm naudojant gas_station ir pradinius duomenis
        form_gas_station = EditGasStationForm(instance=gas_station, initial=initial_gas_station_data)

    # kas bus perduodama su context
    context = {
        'form_car': form_car,
        'form_gas_station': form_gas_station,
        'carmileage_id': carmileage_id
    }
    # grazinam visa info (context) i url
    return render(request, 'manoApps/edit_car.html', context)


@login_required  # tikrina ar prisijunges
def delete_car(request, car_id, gas_station_id):
    # gaunam UserCar pagal car_id ir prisijungusi useri
    user_car = get_object_or_404(UserCar, id=car_id, user=request.user)
    # gaunam GasStation pagal gas_station_id ir prisijungusi useri
    gas_station = get_object_or_404(GasStation, id=gas_station_id, user_car=user_car)

    # skaiciuojam kiek yra GasStation
    initial_count = user_car.gasstation_set.count()

    # trinam pazymeta GasStation
    gas_station.delete()

    # skaiciuojam GasStation po istrynimo
    final_count = user_car.gasstation_set.count()

    # jeigu 0 trinam ir UserCar
    if initial_count == 1 and final_count == 0:
        user_car.delete()
    # grazina i url
    return redirect('your_car_info')


@login_required  # tikrina ar prisijunges
def add_mileage(request, user_car_id):
    # gaunam original_user_car pagal user_car_id
    original_user_car = get_object_or_404(UserCar, id=user_car_id)
    # pradiniai duomenys su siandien
    initial_data = {'date': date.today()}

    # tikrinam ar POST uzklausa
    if request.method == 'POST':
        # sukuriam AddMileageForm naudoajnt POST duomenis pagal user ir user_car_id
        form = AddMileageForm(request.POST, user=request.user, user_car_id=user_car_id)

        # tikrinam ar gerai uzpildyta
        if form.is_valid():
            # nauja rida
            new_odometer_value = form.cleaned_data['odometer_value']
            # paskutine CarMileage rida pagal user_car_id, rusiuoti pagal ID mazejancia tvarka
            last_car_mileage = CarMileage.objects.filter(user_car_id=user_car_id).order_by('-id').first()
            # paskutine rida is last_car_mileage jei nera 0
            last_odometer_value = last_car_mileage.odometer_value if last_car_mileage else 0

            # skaiciuojam nuvaziuota atstuma
            driven_distance = new_odometer_value - last_odometer_value

            # gaunam degalines pavadinima
            gas_station_name = form.cleaned_data['gas_station_name']

            # tikrinam ar gas_station_name yra GasStationName
            if not isinstance(gas_station_name, GasStationName):
                # priskiriam nauja gas_station_name
                new_gas_station_name = GasStationName(name=gas_station_name)
                # issaugom db
                new_gas_station_name.save()
            else:
                # jeigu yra naudojam kas yra
                new_gas_station_name = gas_station_name

            # sukuriam GasStation su nurodytais laukais
            gas_station = GasStation(
                name=new_gas_station_name.name,
                location=form.cleaned_data['gas_station_location'],
                date=form.cleaned_data['date'],
                user_car=original_user_car,
            )
            # issaugom db
            gas_station.save()

            # sukuriam CarMileage su nurodytais laukais
            car_mileage = CarMileage(
                user_car=original_user_car,
                gas_station=gas_station,
                odometer_value=new_odometer_value,
                fuel_in_tank=form.cleaned_data['fuel_in_tank'],
                driven_distance=driven_distance,
                price=form.cleaned_data['price'],
            )
            # issaugom db
            car_mileage.save()

            # grazinam i url
            return redirect('your_car_info')
    else:
        # sukuriam AddMileageForm su pradiniais duomenimis pagal user ir user_car_id
        form = AddMileageForm(initial=initial_data, user=request.user, user_car_id=user_car_id)

    # grazinam i url su formos ir original_user_car duomenimis
    return render(request, 'manoApps/add_mileage.html', {'form': form, 'user_car': original_user_car})


@login_required  # tikrina ar prisijunges
def mano_service(request):
    # gaunam CarServiceEvent pagal user
    services = CarServiceEvent.objects.filter(user=request.user)
    # grazinam i url su services duomenim
    return render(request, 'manoApps/mano_service.html', {'services': services})


@login_required  # tikrina ar prisijunges
def service_new(request):
    # gaunam CarModel pagal user
    user_cars = CarModel.objects.filter(usercar__user=request.user).values_list('id', flat=True).distinct()
    # tikrina ar neturi auto
    if user_cars.count() == 0:
        # jeigu neturi nukreipia i add_car
        return redirect('add_car')

    # tikrinam ar POST uzklausa
    if request.method == "POST":
        # sukuriam CarServiceEventForm pagal POST duomenis ir user
        form = CarServiceEventForm(request.user, request.POST)
        # tikrinam forma
        if form.is_valid():
            # issaugom forma, bet neirasom i db
            service = form.save(commit=False)
            # esama user priskiriam service.user
            service.user = request.user
            # issaugom i db
            service.save()
            # nukreipiam i url
            return redirect('mano_service')
    else:
        # tikrinam kiek turi user_cars, ar daugiau nei 1
        if user_cars.count() > 1:
            # sukuriam CarServiceEventForm pagal user
            form = CarServiceEventForm(request.user)
        # tikrinam ar turi tik 1
        elif user_cars.count() == 1:
            # sukuriam CarServiceEventForm pagal user ir pradinius duomenis
            form = CarServiceEventForm(request.user, initial={'car': user_cars.first()})

    # grazinam i url su duomenim is formos
    return render(request, 'manoApps/service_new.html', {'form': form})


@login_required  # tikrina ar prisijunges
def service_edit(request, service_id):
    # gaunam CarServiceEvent pagal service_id
    service = get_object_or_404(CarServiceEvent, id=service_id)
    # tikrinam ar POST uzklausa
    if request.method == 'POST':
        # sukuriam CarServiceEventForm pagal POSt duomenis, user ir esama ivyki
        form = CarServiceEventForm(request.user, request.POST, instance=service)
        # tikrinam
        if form.is_valid():
            # issaugom
            form.save()
            # nukreipiam
            return redirect('mano_service')
    else:
        # sukuriam CarServiceEventForm pagal user ir esama ivyki
        form = CarServiceEventForm(request.user, instance=service)

    # grazinam i url su duomenim is formos
    return render(request, 'manoApps/service_edit.html', {'form': form})


@login_required  # tikrina ar prisijunges
def service_delete(service_id):
    # gaunam CarServiceEvent pagal service_id
    service = get_object_or_404(CarServiceEvent, id=service_id)
    # trinam is db
    service.delete()
    # grazina i url
    return redirect('mano_service')


def apie(request):
    # nukreipia i url
    return render(request, 'manoApps/apie.html')


def kontaktai(request):
    # nukreipia i url
    return render(request, 'manoApps/kontaktai.html')
