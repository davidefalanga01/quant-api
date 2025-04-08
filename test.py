#!/usr/bin/env python3

'''
Reimplementing the trading strategy presented in 
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622

Based on the well-known Opening Range Breakout (ORB) strategy
'''
import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

# Getting the dataset Nasdaq 100 Index
stock = yf.Ticker('QQQ')
df = stock.history(period='max', interval='5m')

print(df.head())

# Data cleaning
df.reset_index(inplace=True)
print(df.info())

df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True).dt.tz_convert('US/Eastern').dt.tz_localize(None)
print(df.head())

df['day'] = df['Datetime'].dt.date
df['time'] = df['Datetime'].dt.time

# Check the closing candels time
print(df.sort_values(by='Datetime').groupby('day').last()['time'].value_counts())

# List only entire days
entire_days = df[df['time'] == dt.time(15, 55, 00)]['day'].to_list()
df = df[df['day'].isin(entire_days)]

# The strategy
useful_cols = ['Datetime', 'day', 'time', 'Open', 'Low', 
                'High', 'Close', 'Volume']
# Select two candles
first_candles = df[df['time'] == dt.time(9, 30, 00)][useful_cols]
second_candles = df[df['time'] == dt.time(9, 35, 00)][useful_cols]

# Select the last candle
last_candle = df.groupby('day').last().reset_index()[useful_cols]

# Merge them in single rows
trades = first_candles.merge(second_candles, how='left', on='day', suffixes=['_first', '_second'])
trades = trades.merge(last_candle, how='left', on='day')
print(trades.head())

# Decide the position of the day
trades['position'] = np.sign(trades['Close_first'] - trades['Open_first'])

trades['profit'] = trades['position'] * (trades['Close'] - trades['Open_second'])

plt.plot(trades.index, trades['profit'].cumsum())
plt.show()

# Calculate the cumulative gain
print(trades['profit'].cumsum())

# Avg gain for trade
print("Average profit from trade:", trades[trades['position'] != 0]['profit'].mean())