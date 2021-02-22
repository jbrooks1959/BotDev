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
period = 5
# in_position = False
trade_symbol = "btcusdt"
trade_in_dollars = "Yes"
trade_using_percent_of_wallet = "Yes"
trade_quantity = 0.05  # Can be % of wallet





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
    #close_df = close_df.rename(column = {'0':'Close'})
    #close_df['close'] = closes_df[0]
    #print(closes_df.head())
    #Hull Moving Average
    #Integer(SquareRoot(Period)) WMA [2 x Integer(Period/2) WMA(Price) - Period WMA(Price)]
    #hullma = wma(2 * wma(src1, np.int(len1 / 2)) - wma(src1, len1), np.int(np.sqrt(len1)))
    #data_df['EMA'] = data_df[close].ewm(span=21, adjust=False).mean()
    #DataFrame.rolling(21, min_periods=21, freq=None, center=False, win_type=None, on=Close, axis=0, closed=None)
    #weight = np.arrange(1, 28) #this creates an array with integers 1 to 10 included
    #data_df['WMA'] = data_df.apply(lambda Close: np.dot(Close, weight)/weight.sum(), raw=True)
    #data_df.head()
    #data_df['SMA 9'] = smma[1] * (len - 1) + src) / len
    
    data_df['SMA 9'] = np.round(data_df['Close'].rolling(window=9).mean())
    data_df['SMA 21'] = np.round(data_df['Close'].rolling(window=21).mean())
    data_df['EMA 21'] = np.round(data_df.loc[0:, 'SMA 21'].ewm(span=21, adjust=False).mean())
        
    #print(data_df.head())
    print(data_df)
    
    
    #sma = sum(closes) / len(closes)
    print("EMA of Closes")
    #display(data_df.dtypes) 
    #src1 = 'Close'
    #len1 = 21
    #data_df = int(np.sqrt(len1) * data_df['EMA'] * [2 * int(len1/2)])
    #data_df['hullma'] = data_df['EMA'](2) # * data_df['EMA'](src1, int(len1 / 2)) - data_df['EMA'](src1, len1), int(np.sqrt(len1)))
    #print(data_df['Closes']['EMA'])

ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
