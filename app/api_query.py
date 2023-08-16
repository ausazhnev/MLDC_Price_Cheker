from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup as bs

def get_price(brand, pn) -> float | str:
    connect = 'http://api.rossko.ru/service/v2.1/GetSearch'
    headers = {'content-type': 'application/soap+xml'}
    body = f'<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
           f'xmlns:api="http://api.rossko.ru/">' \
           f'<soapenv:Header/>' \
           f'<soapenv:Body>' \
           f'<api:GetSearch>' \
           f'<api:KEY1>{os.getenv("KEY1")}</api:KEY1>' \
           f'<api:KEY2>{os.getenv("KEY2")}</api:KEY2>' \
           f'<api:text> {brand} {pn}</api:text>' \
           f'<api:delivery_id>000000001</api:delivery_id>' \
           f'<!--Optional:-->' \
           f'<api:address_id></api:address_id>' \
           f'</api:GetSearch>' \
           f'</soapenv:Body>' \
           f'</soapenv:Envelope>'
    response = requests.post(connect, headers=headers, data=body)
    soap_answer = bs(response.text, 'xml')
    if soap_answer.find('ns1:success') != None and soap_answer.find('ns1:success').text != 'false':
        if soap_answer.find("ns1:price") != None:
            price = float(soap_answer.find("ns1:price").text)
            return price
        else:
            answer = f'это продано {brand} {pn}'
            return answer
    else:
        answer = f'эчто то пошло не так для {brand} {pn}'
        return answer
