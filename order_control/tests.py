import json

from django.test import TestCase
import requests
# Create your tests here.

# Pega token na API
class getToken():

    def authenticate( username, password):

        credentials = {
            "username" : username,
            "password" : password
        }

        response = requests.post("http://127.0.0.1:8000/api/token/", data=credentials)

        return response.json()

authentication = getToken.authenticate('aline', '49*kj04/')

if authentication['access']:
    access = authentication['access']
refresh = authentication['refresh']

#print("refresh: ", refresh)

url="http://127.0.0.1:8000/api/orders/"
headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
}

resposta = requests.get(url, headers)

#print(resposta.json()['maxPage'])
for resp in resposta.json()['results']:
    print(resp)
    # print(resp['client'])
