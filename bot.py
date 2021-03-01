import json
import pprint
import websocket
import pandas as pd
import numpy as np
from datetime import datetime
import time
import math
#import concurrent.futures
#from binance.enums import *
#from binance.client import Client
#import matplotlib.pyplot as plt
start = time.perf_counter()



socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"


closes = []
vols = []
candles = pd.DataFrame()
in_position = False


period = 21 
#weight = period * (period +1)/2
#print("Weight Factor is:")
#print(weight)

trade_symbol = "btcusdt"
trade_in_dollars = "Yes"
trade_using_percent_of_wallet = "Yes"
trade_quantity = 0.05  # Can be % of wallet

def weight(data, period):
    weight = period * (period +1)/2
    return weight

''' Calculates Weighted Moving Average, series is the specific data (Candle Closed)
values, period is the number of candles in a timeframe that have to have completed'''
def wma(series, period):
    return series.rolling(period).apply(
        lambda prices: np.dot(prices, np.arange(1, period + 1)) / np.arange(1, period + 1).sum(), raw=True)

'''Develops the BUY/Sell signal to be traded on using the candles dataframe closed
data, delay is the number of candles that have to complete to perform calculation
src is the source of the data'''
#def signal(self):
#        df = self.candles
#        delay = 10
#        src = df['Close']

#        hullma = wma(2 * wma(src, int(delay / 2)) - wma(src, delay), int(np.sqrt(delay)))

#        if hullma[-1] > hullma[-2]:
#            hnum = 1
#            print('BUY')
#        else:
#            hnum = 0

#        if hnum == 1:
#            return 1
#        elif hnum == 0:
#            return -1
#        else:
#            return 0

def numpy_ewma_vectorized_v2(data, window):

    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    n = data.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1/pows[:-1]
    offset = data[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out


def on_open(ws):
    print('Connection Established')


def on_close(ws):
    print("Connection Terminated")


def on_message(ws, message):
    global closes, period, candles

    json_message = json.loads(message)
    candle = json_message["k"]
    
    data = pd.DataFrame.from_dict(candle, orient ='index')

    data = pd.DataFrame(candle.items(), columns = ['Label', 'Value'])
   
    pd.set_option('display.max_columns', None)
    data.replace({'s':'Symbol', 'o':'Open', 'c':'Close',\
         'h':'High', 'l':'Low', 'v':'Volume', 'n':'#Trades'}, inplace=True)

    data = data.loc[[6,7,8,9,10,11]].set_index('Label').T.apply(pd.to_numeric).astype('int64')
    data = data.assign(SMS_21='', EMA_21='', WMA='', Range='', Range_60='', Hull_MA='', Signal='')
    #print(data)
    #data = data.iloc[[6,7,8,9,10,11]].set_index('Label').T.astype('int64')
    #print(candles.tail(4))
    candles = candles.append(data, ignore_index=True)
    #candles = candles.assign(SMS_21='', EMA_21='', WMA='', Range='', Range_60='', HUll_MA='', Signal='')
    
    print(candles.tail(4))
   
    src = candles.Close
    
    candles['SMA_21'] = src.rolling(window=21).mean()
    #candles['EMA_21'] = src.ewm(span=21, adjust=True,  min_periods=21, axis=0).mean()
    candles['EMA_21'] = numpy_ewma_vectorized_v2(src, 21)
    candles["WMA"] = wma(src, 21)
    candles['Range'] = src.iloc[-1] - candles.Open.iloc[-2]
    
    candles['Range_60'] = src.iloc[-1] - candles.Open.iloc[-30].mean()
    #print(candles.tail(4))
    #print(candles.tail(4))
    #candles["Hull_MA"] = wma(2 * wma(src, 10 / 2) - wma(src, 10), np.sqrt(10))
    if candles['Volume'].iloc[-1] > 7:
       candles['Vol_Good'] = True
       
    if candles['Range'].iloc[-1] > 15 or candles['Range'].iloc[-1] < -15:
        candles['Range_Good'] = True
    #print(candles.tail(4))
    hullma = wma(2 * wma(src, int(10 / 2)) - wma(src, 10), int(np.sqrt(10)))
    candles["Hull_MA"] = hullma
    #candles["Hull_MA"] = candles.WMA(2 * candles.WMA(src, 10 / 2) - candles.WMA(src, 10), np.sqrt(10))
    
    
    if candles['Hull_MA'].iloc[-1] > candles['Hull_MA'].iloc[-2] and candles['Vol_Good'] == True:
        candles['Signal'] = 'BUY'
    elif candles['Hull_MA'].iloc[-1] < candles['Hull_MA'].iloc[-2] and candles['Range_Good'] == True:
        candles['Signal'] = 'SELL'
    else:
        candles['Signal'] = 'WAIT'
        
    
    #finish = time.perf_counter()
    # print(f'Finished in {round(finish-start, 2)} second(s)')
    #signal(candles)
    
     
    
    

ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
