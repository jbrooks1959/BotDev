# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:21:48 2021

@author: Administrator
"""
import pandas as pd
import numpy as np
from pybit import WebSocket
from time import sleep
from pandas import DataFrame, Series
from indicators import TA
stream = pd.DataFrame()


closes = []
vols = []

in_position = False


period = 21 

# ws = WebSocket("wss://stream.bybit.com/realtime", subscriptions=["klineV2.1.BTCUSD"])

# Define your endpoint URL and subscriptions.
endpoint = 'wss://stream.bybit.com/realtime'
subs = ["klineV2.1.BTCUSD"]

# Connect without authentication!
ws = WebSocket(endpoint, subscriptions=subs)

# This is the script
while True:
    sleep(60)
    pd.set_option('display.max_columns', None)
    message = {i: ws.fetch(i) for i in subs}
    df = pd.DataFrame.from_dict(message, orient ='index')
    try:
        df.drop(df.columns[[0,1,7,8,9]], axis=1, inplace=True)
    except:
        pass
    stream = stream.append(df, ignore_index=True)
    #print('\n'*20,stream.tail())
    print('\n'*10,stream.tail().fillna(0))
    
    stream['Vol_Good'] = stream['volume'].apply(lambda x: 1 if x > 678744 else 0)
    #print(type(stream['Vol_Good']))
    
    
    src = stream.close
    ohlc = stream
    ohlc = ohlc.rename(columns=str.lower)
    stream['SMA_21'] = TA.SSMA(ohlc, period)
    stream['EMA_21'] = TA.EMA(ohlc, period)
    stream['WMA'] = TA.WMA(ohlc, 10)
    stream['HMA'] = TA.HMA(ohlc, 2)
    
        
    stream['Range'] = src - stream['open']
    stream['AvgRange'] = stream['Range'].rolling(window=21).mean()
   
    try:
        if stream['HMA'].iloc[-1] > stream['HMA'].iloc[-2] and stream['Vol_Good'].iloc[-1] == 1:
            stream['Signal'] = "BUY"
            
        elif stream['HMA'].iloc[-1] < stream['HMA'].iloc[-2] and stream['Vol_Good'].iloc[-1] == 1:
            stream['Signal'] = "SELL"
        else:
            stream['Signal']= 'WAIT'
    except:
        pass