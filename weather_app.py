import requests
import json
import pprint as pt

accuweatherAPIKey = 'JMXCPnfdkcPbmHyJ3EUyQ48dZe3bYZVm'

r = requests.get('http://www.geoplugin.net/json.gp')

if(r.status_code!=200):
    print('Não foi possível obter a localização.')
    exit()
else:
    ##json.loads converte o r.text, que é uma str, para um dicionário: chave-valor.
    localizacao = json.loads(r.text)
    ##print(pt.pprint(localizacao))
    latitude = localizacao['geoplugin_latitude'] 
    longitude = localizacao['geoplugin_longitude']

#Utilizando API para descobrir o código referente a latitude e longitude.
localizationAPI = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+accuweatherAPIKey+'&q='+latitude+'%2C%20'+longitude+'&language=pt-br'

rGeoPosition = requests.get(localizationAPI)

if(rGeoPosition.status_code!=200):
    print('Não foi possível obter a localização')
else:
    #só peguei o código e a cidade, estado e país
    r2 = json.loads(rGeoPosition.text)
    
    nomeLocal = r2['LocalizedName'] + ', ' + r2['AdministrativeArea']['LocalizedName'] + '. ' + r2['Country']['LocalizedName'] +'.'

    codGeoPositon = r2['Key']
    print('Local:',nomeLocal)
    print('Codigo:',codGeoPositon)

