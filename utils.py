#!/usr/bin/python3
"""

"""

import pandas as pd
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI, API_KEY_COINMARKETCAP
from datetime import datetime, date
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def get_USD(today):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    url = 'https://trm-colombia.vercel.app/?date={}}'.format(today)

    try:
        response = requests.get(url).json()
    except Exception as e:
        print(e)

    return response['data']['value']

def get_cryptocurrency():
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY_COINMARKETCAP,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return data

def get_criptos(data, i):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    symbol = data['data'][i]['symbol']
    rank = data['data'][i]['cmc_rank']
    price = data['data'][i]['quote']['USD']['price']
    name = data['data'][i]['name']

    return name, symbol, rank, price

def create_df(data):
    """sumary_line

    Keyword arguments:
    argument -- description
    Return: return_description
    """
    col = ['name', 'symbol', 'rank', 'price_USD']
    df = pd.DataFrame(data, columns=col)
    df.set_index('rank', inplace=True)

    return df

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,today,usd, df):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body='\nHola! \n\n\n El valor del dolar hoy '+ today +' es ' + usd +' y las criptomonedas mejor \
                            ranqueadas son : \n\n\n ' + str(df),
                        from_='whatsapp:'+PHONE_NUMBER,
                        to='whatsapp:+573132323026'
                    )

    return message.sid