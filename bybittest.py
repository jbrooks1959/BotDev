# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:21:48 2021

@author: Administrator
"""
import json
import pandas as pd
import numpy as np
#import websocket
from pybit import WebSocket
from time import sleep
import time as time
from datetime import datetime
feed = []
candles = pd.DataFrame()
#ws = WebSocket("wss://stream.bybit.com/realtime", subscriptions=["klineV2.1.BTCUSD"])
ws = WebSocket("wss://stream.bybit.com/realtime", subscriptions=["klineV2.1.BTCUSD"])
#socket = "wss://stream.bytick.com/realtime"
#print(ws)
print(ws)
def on_open(ws):
    print('Connection Established')


def on_close(ws):
    print("Connection Terminated")



def on_message(ws, message):
    global closes, period, candles
    json_message = json.loads(message)
    print(json_message)
    #walletbal[0]['result']['EOS']['wallet_balance']
    #candle = json.loads(message)
    #data = pd.DataFrame.from_dict(candle, orient ='index')
    #message = ws.fetch("klineV2.1.BTCUSD")
    #print(message)
while True:
    message = ws.fetch("klineV2.1.BTCUSD")
    json_message = message
    #candle = json_message
    print(json_message)
    data = pd.DataFrame.from_dict(message, orient ='index')
    #print(data)
    #--------------------------------------Test COde
    #data = pd.DataFrame(candle.items(), columns = ['Label', 'Value'])
   
    #pd.set_option('display.max_columns', None)
    #pd.options.display.float_format = '{:,.0f}'.format
    #data.replace({'s':'Symbol', 'o':'Open', 'c':'Close',\
         #'h':'High', 'l':'Low', 'v':'Volume', 'n':'#Trades'}, inplace=True)

    #data = data.iloc[[6,7,8,9,10,11]].set_index('Label').T.apply(pd.to_numeric).astype('int64')
    #data = data.assign(SMA_21='', EMA_21='', WMA='', Range='', Range_60='', Hull_MA='', Signal='', Vol_Good='', Range_Good='', Confirm='')
    
    #candles = candles.append(data, ignore_index=True)
    #print('\n'*10,candles.tail().head(4).fillna(0))

    #ohlc = candles
    #ohlc = ohlc.rename(columns=str.lower)
    #candles['SMA_21'] = TA.SSMA(ohlc, period)
    #candles['EMA_21'] = TA.EMA(ohlc, period)
    #candles['WMA'] = TA.WMA(ohlc, period)
    #candles['HMA'] = TA.HMA(ohlc, period)
   
      
   
   
    #print('\n'*10,candles.tail().head(8).fillna(0))
    #print(candles.tail(8))
    #----------------------------------End Test Code----------------------------------
    
    #print(type(message))
    #print(message)  
     #message = ws.fetch("klineV2.1.BTCUSD")
     #data = pd.DataFrame.from_dict(message, orient ='index')
     #sleep(1)
     #print(message[0]['open'])

     #feed.append(message)
     #sleep(1)
     #print(data)
     #print(message)
#     time.sleep(1)
#for x in range(5):
#     if message:
#      for i in message:
#           if i not in feed:
#                feed.append(i)
#      print(feed)
     #else:
     #     pass #print("Done")

#print(feed)
#sleep(1000)
#print(feed)

    #ws = WebSocket(socket, on_open=on_open, on_close=on_close, on_message=on_message)
    #ws.run_forever()