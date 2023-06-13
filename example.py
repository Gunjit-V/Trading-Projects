"""
    Created on Monday Feb 2 2022

    @author: Nishant Jain

    :copyright: (c) 2022 by Angel One Limited
"""
import pyotp
from config import *
from smartapi import SmartConnect
from smartWebSocketV2 import SmartWebSocketV2

obj = SmartConnect(apikey)

data = obj.generateSession(clientId, password, pyotp.TOTP(otp_token).now())

FEED_TOKEN = obj.getfeedToken()
CLIENT_CODE = clientId
AUTH_TOKEN = data['data']['jwtToken']
API_KEY = apikey

correlation_id = "test"
action = 1
mode = 2

token_list = [{"exchangeType": 2, "tokens": ["35003"]}]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)


def on_data(wsapp, message):
    print("Ticks: {}".format(message))


def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)


def on_error(wsapp, error):
    print(error)


def on_close(wsapp):
    print("Close")


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()
