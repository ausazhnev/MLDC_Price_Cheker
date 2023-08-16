import sqlite3 as sq
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup as bs
from datetime import date


def set_prise_date(price_id, price) -> None:
    my_date = date.today()
    cur.execute('UPDATE price_list SET act_date = ?, price = ? WHERE id = ?', (my_date, price, price_id,))
    con.commit()
    print(f'Информация для id {price_id} обновлена')


def get_elem_data(data_list) -> None:
    for elem in data_list:
        print(elem)
        connect = 'http://api.rossko.ru/service/v2.1/GetSearch'
        headers = {'content-type': 'application/soap+xml'}
        body = f'<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
               f'xmlns:api="http://api.rossko.ru/">' \
               f'<soapenv:Header/>' \
               f'<soapenv:Body>' \
               f'<api:GetSearch>' \
               f'<api:KEY1>{os.getenv("KEY1")}</api:KEY1>' \
               f'<api:KEY2>{os.getenv("KEY2")}</api:KEY2>' \
               f'<api:text> {elem[1]} {elem[2]}</api:text>' \
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
                set_prise_date(elem[0], price)
            else:
                print(f'это продано {elem[1]} {elem[2]}')
        else:
            print('что то пошло не так')


def get_nomenclature_list() -> list:
    cur.execute('SELECT id, brand, pn FROM price_list')
    results = cur.fetchall()
    return results


try:
    con = sq.connect('../db/mldc.db')
    cur = con.cursor()
    flag = True
except sq.Error as err:
    print(err)
load_dotenv()
prod_list = get_nomenclature_list()
get_elem_data(prod_list)
if flag: con.close()
