# Cryptocurrency Library 
#
# (c) 2022 by QuantAtRisk

#  __all__ = ['getCryptoSeries']

import numpy as np
import pandas as pd

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


def timestamp2date_hms(timestamp):
    # function converts a Unix timestamp into Gregorian date
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M')


def getCryptoSeries(tsym, fsym='USD', freq='d', ohlc=False, exch='CCCAGG', start_date='2015-01-01', end_date=None):
    
    ccpair = tsym + fsym
    
    if freq == 'd':
        str_freq = 'histoday'
        lab = '1D'
    elif freq == 'm':
        str_freq = 'histominute'
        lab = '1MIN'
    elif freq == 'h':
        str_freq = 'histohour'
        lab = '1H'
    else:
        print('Error: wrong frequency code.')
        return None
        # raise RuntimeError("dummy error") -> better off with this command

    
    if not(end_date):
        now = datetime.now()  # date and time now
        tda = datetime.today()
        tda = tda.replace(hour=0, minute=0, second=0, microsecond=0)
        
        if freq == 'm':
            end_ts = now.timestamp()
            end_dt = pd.to_datetime(now, format='%Y-%m-%d %H:%M:%SS')
        elif freq == 'd':
            end_ts = tda.timestamp()
            end_dt = pd.to_datetime(tda, format='%Y-%m-%d')
        elif freq == 'h':
            end_ts = now.timestamp()
            end_dt = pd.to_datetime(now, format='%Y-%m-%d %H:%M')
    else:
        if freq == 'm':
            end_dt = pd.to_datetime(end_date, format='%Y-%m-%d %H:%M:%S')
            if len(end_date) > 10:
                end_ts = datetime.strptime(end_date, '%Y-%m-%d %H:%M').timestamp()
            elif len(end_date) == 10:
                end_ts = datetime.strptime(end_date, '%Y-%m-%d').timestamp()
        elif freq == 'd':
            end_dt = pd.to_datetime(end_date, format='%Y-%m-%d') 
            end_ts = datetime.strptime(end_date, '%Y-%m-%d').timestamp()
        elif freq == 'h':
            end_dt = pd.to_datetime(end_date, format='%Y-%m-%d %H:%M')
            if len(end_date) > 10:
                end_ts = datetime.strptime(end_date, '%Y-%m-%d %H:%M').timestamp()
            elif len(end_date) == 10:
                end_ts = datetime.strptime(end_date, '%Y-%m-%d').timestamp()
            
            
    start_dt = pd.to_datetime(start_date, format='%Y-%m-%d %H:%M')
    t0 = pd.to_datetime('2015-01-01', format='%Y-%m-%d')
    if start_dt < t0:
        start_dt = t0
    
    if len(start_date) > 10:
        start_ts = datetime.strptime(start_date, '%Y-%m-%d %H:%M').timestamp()
    elif len(start_date) == 10:
        start_ts = datetime.strptime(start_date + ' 00:00', '%Y-%m-%d %H:%M').timestamp()
    start_dt = datetime.fromtimestamp(int(start_ts)).strftime('%Y-%m-%d %H:%M')
    
    if end_date is not None:
        if len(end_date) > 10:
            end_ts = datetime.strptime(end_date, '%Y-%m-%d %H:%M').timestamp()
        elif len(start_date) == 10:
            end_ts = datetime.strptime(end_date + ' 00:00', '%Y-%m-%d %H:%M').timestamp()
        end_dt = datetime.fromtimestamp(int(end_ts)).strftime('%Y-%m-%d %H:%M')
    
    ok = True
    fi = True
    
    while ok:    
        url = "https://min-api.cryptocompare.com/data/v2/" + str_freq + "?fsym=" + tsym + \
                      "&aggregate=1&tsym=" + fsym + "&toTs=" + str(int(end_ts)) + "&limit=2000" + "&e=" + exch + \
                      "&api_key=62e25e00009657bade066be68957052c248aaded31a8bda345bf3f497c783b08"
        #print(url)
        
        # fetch the raw data
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())  # convert from json to dictionary

        try:
            data = dic['Data']['Data']
        except:
            dd = dd[dd.index <= end_dt]
            return dd
            
        df = pd.DataFrame(data)
        df['date'] = df.time.apply(timestamp2date_hms)  
        
        # update end_ts
        end_ts = df.head(1)[['date', 'time']].iloc[0,1]

        if ohlc:
            df = df[['date', 'open', 'high', 'low', 'close']]
            df.rename(columns = {df.columns[1] : ccpair+'_O',
                                 df.columns[2] : ccpair+'_H',
                                 df.columns[3] : ccpair+'_L',
                                 df.columns[4] : ccpair+'_C'}, inplace=True)
        else:
            df = df[['date', 'close']]
            df.rename(columns = {df.columns[1] : ccpair}, inplace=True)
        df.index = pd.to_datetime(df.date, format='%Y-%m-%d %H:%M')
        df.drop('date', axis=1, inplace=True)
        
        df = df[(df.index >= start_dt) & (df.index <= end_dt)]
        
        if fi:
            dd = df.copy()
            fi = False
        else:
            dd = pd.concat([dd, df])
                
        dd = dd[dd.values > 0]
        dd.sort_index(inplace=True)
        #if freq == 'h':
        #    dd.index = dd.index + pd.DateOffset(hours=1)

        dd.drop_duplicates(inplace=True)
        
        if end_ts <= start_ts:
            ok = False
            dd = dd[dd.index <= end_dt]
            return dd

            