from django.shortcuts import render


def home_url(request):
    return render(request=request, template_name='home.html')
