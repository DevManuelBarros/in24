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

def putData(url,  data, method='POST'):
    session = requests.Session()
    req = requests.Request(method, url, headers=pHeaders, data=data)
    response = session.send(req.prepare(), verify=True)
    return response.status_code

def saveR(n):
    for k, v in n.items():
        for Kitems, Vitems in n[k].items():
            if Kitems == 'pictures':
                print('Grabando {}-{}'.format(Kitems,k))
                for K in Vitems:
                    putData(dicEnlaces['pictures'], data=json.dumps(K))
            else:    
                j = json.dumps(Vitems)
                print('Grabando {}-{}:->{}'.format(Kitems,k, putData(dicEnlaces[Kitems], data=j)))
                    

