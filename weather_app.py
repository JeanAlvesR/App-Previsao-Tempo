import requests
import json
import pprint as pt
r = requests.get('http://www.geoplugin.net/json.gp')

if(r.status_code!=200):
    print('Não foi possível obter a localização.')
else:
    #json.loads converte o r.text, que é uma str, para um dicionário: chave-valor.
    localizacao = json.loads(r.text)
    #print(pt.pprint(localizacao))
    latitude = localizacao['geoplugin_latitude'] 
    longitude = localizacao['geoplugin_longitude']
    print('Latitude:',latitude,'Logitude:',longitude) 