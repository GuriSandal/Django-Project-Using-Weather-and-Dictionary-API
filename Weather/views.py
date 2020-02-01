from django.shortcuts import render,get_object_or_404
import requests
from Weather.models import City,UserData
from Weather.forms import CityForm,UserForm
from django.http import HttpResponseRedirect,HttpRequest,HttpResponse
from django.urls import reverse
from django.contrib import messages
from Weather import forms

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=21e696f4e0e757c95340595f106183b3'
    urlMap = 'https://open.mapquestapi.com/staticmap/v5/map?key=SmG71tZTSw5l2rXpFspwnYQq7Vy0jJPO&center={},{}&size=@2x'
    cities = City.objects.order_by('name')
    form = CityForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('main')
        except:
            return HttpResponse("""<script>alert('Sorry City Name not found with our database');
            window.location = "http://127.0.0.1:8000/";
            </script>
            """)

    else:
        form = CityForm()

    weather_data = []
    for city in cities:
        print(city.id)
        city_weather = requests.get(url.format(city)).json()
        try:
            Weather = {
                'id' : city.id,
                'city' : city.name,
                'temperature' : city_weather['main']['temp'],
                'pressure' : city_weather['main']['pressure'],
                'humidity' : city_weather['main']['humidity'],
                'clouds' : city_weather['clouds']['all'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon'],
                'wind' : city_weather['wind']['speed'],
                'latitude' : city_weather['coord']['lat'],
                'longitude' : city_weather['coord']['lon'],
                'country' : city_weather['sys']['country'],
            }
            weather_data.append(Weather)
        except:
            city.delete()
            return HttpResponse("""<script>alert('Sorry City Name not found with our database');
            window.location = "http://127.0.0.1:8000/";
            </script>
            """)

    context = {'weather_data' : weather_data, 'form' : form,}
    return render(request, "Weather/index.html", context)


def delete_city(request, id):

    city = get_object_or_404(City, id=id)
    form = CityForm(request.POST, instance=city)
    city.delete()
    return HttpResponseRedirect(reverse('main'))

def form(request):
    form_data = forms.UserForm()

    if request.method == "POST":
        form_data = forms.UserForm(request.POST)

        if form_data.is_valid():
            form_data.save(commit = True)
            return index(request)
            print("Register Successfully")

    return render(request,'Uform.html',context = {'udata':form_data})
