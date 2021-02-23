import json
import pprint
import websocket
import pandas as pd
import numpy as np
from datetime import datetime
#from binance.enums import *
#from binance.client import Client
#import matplotlib.pyplot as plt




socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

closes = []
in_position = False
# vols = []
smaT = []
# src = closes
period = 21
weight = period * (period +1)/2
print("Weight Factor is:")
print(weight)
# in_position = False
trade_symbol = "btcusdt"
trade_in_dollars = "Yes"
trade_using_percent_of_wallet = "Yes"
trade_quantity = 0.05  # Can be % of wallet

def weight(data, period):
    weight = period * (period +1)/2
    return weight


def wma(series, period):
    return series.rolling(period).apply(
        lambda prices: np.dot(prices, np.arange(1, period + 1)) / np.arange(1, period + 1).sum(), raw=True)



print("This is it")
#print(weight(21))

def on_open(ws):
    print('Connection Established')


def on_close(ws):
    print("Connection Terminated")


def on_message(ws, message):
    global closes
    global period
    global tclose
    global smaT
    
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message["k"]
    
    close = candle['c']
    #is_candle_closed = candle["x"]
    closes.append(float(close))
    #print("closes")
    #print(closes)
    data_df = pd.DataFrame(closes, columns = ['Close'])
    series = data_df["Close"]
    #print(series)
    #print("one way")
    #print(weight(data_df['Close'], 21))
    len1 = 10
    src1 = data_df["Close"]
    #hullma = wma(2 * wma(close, np.int(period / 2)) - wma(close, period), np.int(np.sqrt(period))) 
    #print(hullma)
    hullma = wma(2 * wma(src1, np.int(len1 / 2)) - wma(src1, len1), np.int(np.sqrt(len1)))
    data_df['SMA 9'] = np.round(data_df['Close'].rolling(window=9).mean()) # Correct
    data_df['SMA 21'] = np.round(data_df['Close'].rolling(window=21).mean()) #Correct
    data_df['EMA 21'] = np.round(data_df['Close'].ewm( span=21, adjust=True,  min_periods=21, axis=0).mean())
    data_df["WMA"] = np.round(wma(series, 21))
    data_df["Hull MA"] = np.round(hullma)
    print(data_df)
    
    
    

ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
