from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import lxml

# Create your views here.
def weatherUpdates(location):
    header = {
        'User-Agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Language' : 'eng',
    }
    # if location name container spaces then space will be changed to + 
    location = location.replace(' ', "+")
    
    url = f'https://www.google.com/search?q=weather+in+{location}'
    
    # sending request 
    try:
        resp = requests.get(url, headers=header)
        contentdata = resp.content
        soup = BeautifulSoup(contentdata, 'lxml')
        location_name = soup.find('span', attrs={'class':'BBwThe'}).text
        temperature = soup.find('span', attrs={'id':'wob_tm'}).getText()
        precipitation = soup.find('span', attrs={'id':'wob_pp'}).getText()
        humidity = soup.find('span', attrs={'id':'wob_hm'}).getText()
        wind_speed = soup.find('span', attrs={'class':'wob_t'}).getText()
        day_and_time = soup.find('div', attrs={'id':'wob_dts'}).getText()
        
        weather_condition = soup.find('span', attrs={'id':'wob_dc'}).getText()
        
        # create a dictionary from weather data 
        wether_dect = {
            'location':location_name,
            'temperature':temperature,
            'precipitation':precipitation,
            'humidity':humidity,
            'wind_speed':wind_speed,
            'day_and_time':day_and_time,
            'condition':weather_condition
        }
        # return the dictionary to the calling function 
        return wether_dect
    except Exception as e:
        wether_dect = {
            'invalid_location': 'invalid location'
        }
        return wether_dect

def home(request):
    if request.method == "POST":
        location = request.POST.get('location')
        response = weatherUpdates(location)
        
        return render(request, 'weatherapp/index.html', {'response':response})
    return render(request, 'weatherapp/index.html')
    