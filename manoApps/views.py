from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


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
    return render(request, 'manoApps/register.html', {'form': form})


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
    return render(request, 'manoApps/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def logged_home(request):
    return render(request, 'manoApps/mano_home.html')