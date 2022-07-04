import requests
import json
import pprint as pt

accuweatherAPIKey = 'JMXCPnfdkcPbmHyJ3EUyQ48dZe3bYZVm'

r = requests.get('http://www.geoplugin.net/json.gp')

if(r.status_code!=200):
    print('Não foi possível obter a localização.')
    exit()
else:
    #json.loads converte o r.text, que é uma str, para um dicionário: chave-valor.
    localizacao = json.loads(r.text)
    #print(pt.pprint(localizacao))
    latitude = localizacao['geoplugin_latitude'] 
    longitude = localizacao['geoplugin_longitude']
    print('Latitude:',latitude,'Logitude:',longitude) 

rGeoPosition = requests.get('http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+accuweatherAPIKey+'&q='+latitude+'%2C%20'+longitude+'&language=pt-br')

if(rGeoPosition.status_code!=200):
    print('Não foi possível obter a localização')
else:
    print(pt.pprint(rGeoPosition.text))