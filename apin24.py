import requests
import json
import time
pHeaders = {'Content-Type' : 'application/json'}
dicEnlaces = {  'inmuebles' : 'http://localhost:8000/inmuebles/',
                'features' : 'http://localhost:8000/features/',
                'prices' : 'http://localhost:8000/prices/',
                'location' : 'http://localhost:8000/locations/',
                'pictures' : 'http://localhost:8000/pictures/',
                'description' : 'http://localhost:8000/descriptions/'}


def getData(url, method='GET'):
    session = requests.Session()
    req = requests.Request(method, url)
    response = session.send(req.prepare(), verify=True)
    
    return response.json()

def putData(url,  data, method='POST', foo=False):
    session = requests.Session()
    req = requests.Request(method, url, headers=pHeaders, data=data)
    response = session.send(req.prepare(), verify=True)
    if foo==False:
        return response.status_code, response.text
    else:
        return response.text

def saveR(n):
    value = True
    for k, v in n.items():
        inmueble = True
        for Kitems, Vitems in n[k].items():
            if inmueble == True:
                if Kitems == 'pictures':
                    for K in Vitems:
                        result, text = putData(dicEnlaces['pictures'], data=json.dumps(K))
                        if int(result) > 350:
                            print('Error en {}-{} ----> {}'.format(Kitems,k,text))
                            value = False
                        else:
                            print('Ok')
                else:
                    j = json.dumps(Vitems)
                    result, text = putData(dicEnlaces[Kitems], data=j)
                    if int(result) > 350:
                        print('Error en {}-{} ----> {}'.format(Kitems,k,text))
                        value = False
                        if Kitems == 'inmuebles':
                            inmueble = False   
                    else:
                        print('Ok')
                         
    return value
                    
g ={'postingId': '57626800', 'postingCode': '2B49NA', 'title': 'Casa en Venta Bosques de Las Lomas', 'url': '/propiedades/casa-en-venta-bosques-de-las-lomas-57626800.html', 'reserved': False, 'status_online': True, 'type_prop': 'Casa', 'id_scrap': '84840716', 'publication_null_date': '1900-01-01', 'publication_date': '2019-12-12', 'lat': 19.394351, 'lon': -99.24340219999999, 'postingType': 'PROPERTY', 'renta': False, 'sale': True, 'tmp_rent': False}
j = json.dumps(g)
print(putData(dicEnlaces['inmuebles'], data=j, foo=True))