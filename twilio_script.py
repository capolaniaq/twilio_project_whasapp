#!/usr/bin/python3
"""

"""


import os
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from tqdm import tqdm
from datetime import datetime
from utils import *



api_key = API_KEY_WAPI

today = date.today()
usd = get_USD(today=today)
data = get_cryptocurrency()


datos = []

for i in tqdm(range(10), colour='green'):
    datos.append(get_criptos(data, i))


df = create_df(datos)

# Send Message
message_id = send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,today,usd,df)


print('Mensaje Enviado con exito ' + message_id)