from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def get_html_content(city):
    import requests
    API_KEY = "181998a681e3ca84538cb3a52a111b24"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    #we need to get the city we want to get
    url = f"{BASE_URL}?appid={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      weathers = data["weather"][0]["main"]
      weather = data["weather"][0]["description"]
    
      temp = round(data["main"]["temp"] - 273, 2)
      country =  data["sys"]["country"]
      feel = round(data["main"]["feels_like"] - 273, 2)
      all = [weathers,weather,temp,country,city,feel]
    return all
@login_required(login_url='login')
def home(request):
    data = None
    if 'city' in request.GET:
        city= request.GET.get('city')
        alls = get_html_content(city)
        data = dict()
        data["city"]= alls[4]
        data["main"]= alls[0]
        data["description"]= alls[1]
        data["temp"]= alls[2]
        data["country"]= alls[3]
        data["feel"]= alls[5]

    return render(request, "core/home.html", {"data":data})


# to handle 404 errors
def handling_404(request, exception):
    return render(request, 'core/404.html', {})
def error_500(request):
    return render(request, "core/500.html")
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Sing up successfully for ' + user)
            return redirect("login") 
        else:     
            for msg in form.errors:
                ans =str(form.errors[msg]).split("<li>")[1].split("</li>")[0]
                messages.error(request, f"{msg}: {ans}")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form":form,"errors":form.errors})


