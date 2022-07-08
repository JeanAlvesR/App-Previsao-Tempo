import requests
import json
import pprint as pt
from datetime import date

accuweatherAPIKey = 'm2zswr8SjO4dAgWSXBNKjPcVo4S4DwHN'
dias_semana = ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado']

def pegarCoordenadas():

    r = requests.get('http://www.geoplugin.net/json.gp')

    if(r.status_code!=200):
        print('Não foi possível obter a localização.')
        return None
    else:
        try:
            ##json.loads converte o r.text, que é uma str, para um dicionário: chave-valor.
            localizacao = json.loads(r.text)
            ##print(pt.pprint(localizacao))
            coordenadas = {}
            coordenadas['latitude'] = localizacao['geoplugin_latitude'] 
            coordenadas['longitude']= localizacao['geoplugin_longitude']

            return coordenadas

        except:
            return None

        
def pegarCodigo(latitude, longitude):
    #Utilizando API para descobrir o código referente a latitude e longitude.
    localizationAPI = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey='+accuweatherAPIKey+'&q='+latitude+'%2C%20'+longitude+'&language=pt-br'

    rGeoPosition = requests.get(localizationAPI)

    if(rGeoPosition.status_code!=200):
        print('Não foi possível obter a localização')
        return None
    else:
        try:
            #só peguei o código e a cidade, estado e país
            locationResponse = json.loads(rGeoPosition.text)
            nomeLocal = locationResponse['LocalizedName'] + ', ' + locationResponse['AdministrativeArea']['LocalizedName'] + '. ' + locationResponse['Country']['LocalizedName'] +'.'

            codGeoPosition = locationResponse['Key']
            infoLocal = {'nomeLocal': nomeLocal, 'codGeoPosition':codGeoPosition}
            return infoLocal
        except:
            return None

def pegarTempoAgora(codGeoPosition, nomeLocal):

    geoConditionURL = 'http://dataservice.accuweather.com/currentconditions/v1/'+codGeoPosition+'?apikey='+accuweatherAPIKey+'&language=pt-br'


    rTempLocation  = requests.get(geoConditionURL)

    if rTempLocation.status_code !=200:
        print('Não foi possível conectar ao serviço de temperatura')
        return None
    else:
        try:
            currentConditionResponse = json.loads(rTempLocation.text)
            infoClima = {}
            infoClima['temperatura'] = str(currentConditionResponse[0]['Temperature']['Metric']['Value'])+' '+currentConditionResponse[0]['Temperature']['Metric']['Unit']
            infoClima['clima'] = currentConditionResponse[0]['WeatherText']
            infoClima['local'] = nomeLocal

            return infoClima

        except:
            return None


def pegarClima5Dias(codigoLocal):
    climaURL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+codigoLocal+"?apikey="+accuweatherAPIKey+"&language=pt-br&metric=true"

    r = requests.get(climaURL)

    if r.status_code!=200:
        print("Não foi possível acessar os próximos dias")
        return None

    else:
        climaResp = json.loads(r.text)
        listaInfoClima = []
        infoClima = {}
        for i in range (5):
            try:
                infoClima = {}
                infoClima['temperaturaMinima'] = str(climaResp['DailyForecasts'][i]['Temperature']['Minimum']['Value'])
                infoClima['temperaturaMaxima'] = str(climaResp['DailyForecasts'][i]['Temperature']['Maximum']['Value'])
                infoClima['clima'] = climaResp['DailyForecasts'][i]['Night']['IconPhrase']
                infoClima['dia'] = dias_semana[int( date.fromtimestamp( climaResp['DailyForecasts'][i]['EpochDate']).strftime('%w'))]
                listaInfoClima.append(infoClima)
                
            except:
                print('Erro na lista de dicionário')
        return listaInfoClima


## Inicio do Programa
try:
    coordenadas = pegarCoordenadas()
    info = pegarCodigo(coordenadas['latitude'], coordenadas['longitude'])
    climaHoje = pegarTempoAgora(info['codGeoPosition'], info['nomeLocal'])
    listaInfoClima5Dias = pegarClima5Dias(info['codGeoPosition'])

    print('Clima atual em: '+climaHoje['local'])
    print(climaHoje['clima'])
    print('Temperatura: '+climaHoje['temperatura'])

    print('\n\nClima para hoje e para os próximos dias:')
  
    for dia in listaInfoClima5Dias:
        print('\n'+dia['dia'])
        print('Temperatura Máxima: '+dia['temperaturaMaxima'])
        print('Temperatura Mínima: '+dia['temperaturaMinima'])
        print('Clima: '+dia['clima'])



except:
    print('Error!')