import requests
import json
import pprint as pt

accuweatherAPIKey = 'm2zswr8SjO4dAgWSXBNKjPcVo4S4DwHN'


def pegarCoordenadas():

    r = requests.get('http://www.geoplugin.net/json.gp')

    if(r.status_code!=200):
        print('Não foi possível obter a localização.')
        exit()
    else:
        ##json.loads converte o r.text, que é uma str, para um dicionário: chave-valor.
        localizacao = json.loads(r.text)
        ##print(pt.pprint(localizacao))
        coordenadas = {}
        coordenadas['latitude'] = localizacao['geoplugin_latitude'] 
        coordenadas['longitude']= localizacao['geoplugin_longitude']

        return coordenadas
        
def pegarCodigo(latitude, longitude):
    #Utilizando API para descobrir o código referente a latitude e longitude.
    localizationAPI = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+accuweatherAPIKey+'&q='+latitude+'%2C%20'+longitude+'&language=pt-br'

    rGeoPosition = requests.get(localizationAPI)

    if(rGeoPosition.status_code!=200):
        print(rGeoPosition.status_code)
        print('Não foi possível obter a localização')
    else:
        #só peguei o código e a cidade, estado e país
        locationResponse = json.loads(rGeoPosition.text)
        
        nomeLocal = locationResponse['LocalizedName'] + ', ' + locationResponse['AdministrativeArea']['LocalizedName'] + '. ' + locationResponse['Country']['LocalizedName'] +'.'

        codGeoPosition = locationResponse['Key']
        infoLocal = {'nomeLocal': nomeLocal, 'codGeoPosition':codGeoPosition}
        return infoLocal


def pegarTempoAgora(codGeoPosition, nomeLocal):

    geoConditionURL = 'http://dataservice.accuweather.com/currentconditions/v1/'+codGeoPosition+'?apikey='+accuweatherAPIKey+'&language=pt-br'


    rTempLocation  = requests.get(geoConditionURL)

    if rTempLocation.status_code !=200:
        print('Não foi possível conectar ao serviço de temperatura')
    else:
        currentConditionResponse = json.loads(rTempLocation.text)
        infoClima = {}
        infoClima['temperature'] = str(currentConditionResponse[0]['Temperature']['Metric']['Value'])+' '+currentConditionResponse[0]['Temperature']['Metric']['Unit']
        infoClima['climaTexto'] = currentConditionResponse[0]['WeatherText']
        infoClima['nomeLocal'] = nomeLocal

        return infoClima

## Inicio do Programa

coordenadas = pegarCoordenadas()

info = pegarCodigo(coordenadas['latitude'], coordenadas['longitude'])

clima = pegarTempoAgora(info['codGeoPosition'], info['nomeLocal'])

print(pt.pprint(clima))