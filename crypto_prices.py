# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:04:11 2017

@author: ariahklages-mundt

note: data acquisition follows approach from https://blog.patricktriest.com/analyzing-cryptocurrencies-python/
"""

import os
import numpy as np
import pandas as pd
import pickle
import quandl
from datetime import datetime

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as f

################################################################
# quandl API helper functions, used for BTC-to-USD prices
def get_quandl_data(quandl_id):
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/','-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df

################################################################
# poloniex API helper functions, used for altcoin-to-BTC prices
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
    try:        
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df

def merge_dfs_on_column(dataframes, labels, col):
    '''Merge a single column of each dataframe into a new combined dataframe'''
    series_dict = {}
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]
        
    return pd.DataFrame(series_dict)

def get_crypto_data(poloniex_pair, max_tries):
    '''Retrieve cryptocurrency data from poloniex'''
    tries = 0
    while tries < max_tries:
        try:
            json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
            data_df = get_json_data(json_url, poloniex_pair)
            data_df = data_df.set_index('date')
            return data_df
        except:
            tries += 1
    print('Failed to get data: {} in {} attempts'.format(poloniex_pair, max_tries))

################################################################
# Get Bitcoin prices from Quandl and create index
exchanges = ['KRAKEN','COINBASE','BITSTAMP','ITBIT']
exchange_data = {}
for exchange in exchanges:
    exchange_code = 'BCHARTS/{}USD'.format(exchange)
    btc_exchange_df = get_quandl_data(exchange_code)
    exchange_data[exchange] = btc_exchange_df

# Merge the BTC price dataseries' into a single dataframe
btc_usd_datasets = merge_dfs_on_column(list(exchange_data.values()), list(exchange_data.keys()), 'Weighted Price')

# Remove "0" values
btc_usd_datasets.replace(0, np.nan, inplace=True)

# Calculate the average BTC price as a new column
btc_usd_datasets['avg_btc_price_usd'] = btc_usd_datasets.mean(axis=1)

################################################################
# Get altcoin data from Poloniex

base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # up until today
pediod = 86400 # pull daily data (86,400 seconds per day)

#altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM']
#the following are all coins available on Poloniex
#altcoins =['ETH', 'XRP', 'DOGE', 'STR', 'LSK', 'ZEC', 'LTC', 'BCH', 'SC', 'XEM', 'ETC', 'XMR', 'DGB', 'FCT', 'BCN', 'OMG', 'DASH', 'BTS', 'STRAT', 'NXT', 'STEEM', 'ZRX', 'BURST', 'GNT', 'MAID', 'XPM', 'DCR', 'XCP', 'NAV', 'VTC', 'EMC2', 'ARDR', 'LBC', 'SYS', 'GNO', 'PASC', 'STORJ', 'CVC', 'PINK', 'EXP', 'REP', 'GAS', 'GAME', 'POT', 'FLDC', 'OMNI', 'AMP', 'BLK', 'FLO', 'CLAM', 'PPC', 'SBD', 'NEOS', 'BTCD', 'VIA', 'RADS', 'BELA', 'RIC', 'VRC', 'NMC', 'NXC', 'GRC', 'XVC', 'XBC', 'BTM', 'HUC', 'BCY']

#edited list to get longer time series
altcoins =['ETH', 'XRP', 'DOGE', 'STR', 'LSK', 'ZEC', 'LTC', 'BCH', 'SC', 'XEM', 'ETC', 'XMR', 'DGB', 'FCT', 'BCN', 'DASH', 'BTS', 'STRAT', 'NXT', 'STEEM', 'BURST', 'GNT', 'MAID', 'XPM', 'DCR', 'XCP', 'NAV', 'VTC', 'EMC2', 'ARDR', 'LBC', 'SYS', 'GNO', 'PASC', 'PINK', 'EXP', 'REP', 'GAME', 'POT', 'FLDC', 'OMNI', 'AMP', 'BLK', 'FLO', 'CLAM', 'PPC', 'SBD', 'NEOS', 'BTCD', 'VIA', 'RADS', 'BELA', 'RIC', 'VRC', 'NMC', 'NXC', 'GRC', 'XVC', 'XBC', 'BTM', 'HUC', 'BCY']


altcoin_data = {}
for altcoin in altcoins:
    coinpair = 'BTC_{}'.format(altcoin)
    crypto_price_df = get_crypto_data(coinpair,10)
    altcoin_data[altcoin] = crypto_price_df

# Calculate USD Price as a new column in each altcoin dataframe
for altcoin in altcoin_data.keys():
    altcoin_data[altcoin]['price_usd'] =  altcoin_data[altcoin]['weightedAverage'] * btc_usd_datasets['avg_btc_price_usd']

# Merge USD price of each altcoin into single dataframe 
combined_df = merge_dfs_on_column(list(altcoin_data.values()), list(altcoin_data.keys()), 'price_usd')

# Add BTC price to the dataframe
combined_df['BTC'] = btc_usd_datasets['avg_btc_price_usd']


