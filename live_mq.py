from smartWebSocketV2 import SmartWebSocketV2
from smartapi import SmartConnect
from config import *
import pyotp
import datetime as dt
import pika
import time
import threading

# Message Queue Code
connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='ws_data')

obj = SmartConnect(apikey)

data = obj.generateSession(clientId, password, pyotp.TOTP(otp_token).now())
FEED_TOKEN = obj.getfeedToken()
CLIENT_CODE = clientId
AUTH_TOKEN = data['data']['jwtToken']
API_KEY = apikey

token = "nse_fo|35003"
task = "mw"

correlation_id = "test"
action = 1
mode = 2

token_list = [{"exchangeType": 2, "tokens": ["35003"]}]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)



def on_data(wsapp, message):
    try:
        # data = message
        # channel.basic_publish(exchange='', routing_key='ws_data', body=data)
        print(message)
    except Exception as e:
        print(e)


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

threading.Thread(target=sws.connect).start()

time.sleep(10)
sws.unsubscribe("test", 2, token_list)

sws.close_connection()
print("------------------------Connection closed---------------------")