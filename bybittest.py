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
    sleep(10)
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
    stream['OHLC4'] = (stream['open'] + stream['high'] + stream['low'] + stream['close'])/4
    
    try:
        if stream['EMA_21'].iloc[-1] > stream['EMA_21'].iloc[-2]:
                stream.loc[stream.index[-1], 'EMA_Dir'] = "UP"
        #elif stream['EMA_21'].iloc[-1] < stream['EMA_21'].iloc[-2]:
                #stream.loc[stream.index[-1], 'EMA_Dir'] = "DWN"
        else:
            stream.loc[stream.index[-1], 'EMA_Dir'] = "DWN"
            
       
    except:
        pass
     
    
    try:
        if stream['HMA'].iloc[-1] > stream['HMA'].iloc[-2]:
                stream.loc[stream.index[-1], 'HMA_Dir'] = 1
        elif stream['HMA'].iloc[-1] < stream['HMA'].iloc[-2]:
                stream.loc[stream.index[-1], 'HMA_Dir'] = -1
        else:
            stream.loc[stream.index[-1], 'HMA_Dir'] = 0
            
    except:
        pass
        
   
    
    try:
        if stream['HMA'].iloc[-1] > stream['HMA'].iloc[-2]:
            stream['TestSig'] = 1
        else:
            stream['TestSig'] = 0
    except:              
            pass
    stream['Range'] = src - stream['open']
    stream['AvgRange'] = stream['Range'].rolling(window=7).mean()
    stream['AvgHMA'] = stream['HMA'].rolling(window=7).mean()
    try:
        if stream['AvgHMA'].iloc[-1] > stream['AvgHMA'].iloc[-2]: # and stream['HMA_Dir'] > 19.9:  # and stream['EMA_Dir'].iloc[-1] == "UP"
            stream.loc[stream.index[-1], 'Signal'] = "BUY"
           
        elif stream['AvgHMA'].iloc[-1] < stream['AvgHMA'].iloc[-2]: # and stream['EMA_Dir'].iloc[-1] == "DWN"
            stream.loc[stream.index[-1], 'Signal'] = "SELL"
        else:
            stream.loc[stream.index[-1], 'Signal'] = "WAIT"
    except:
        pass
    
    
   