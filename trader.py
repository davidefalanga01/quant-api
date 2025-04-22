import pandas as pd
import yfinance as yf
from tqdm import tqdm

class Trader():
    def __init__(self):
        self.in_buy = 0
        self.in_sell = 0
        self.dates = []
        self.buy_price = 0
        self.sell_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.trades = []
        self.pnl = [0]
        self.buy_prices = []
        self.sell_prices = []
        self.fee = 0
        self.account = 25000
        self.account_history = [self.account]
        self.risk = 0
        self.opening = 0
        self.n_list = []
        self.notionals = [0]
        self.unit_trades = []

    def reset(self):
        self.in_buy = 0
        self.in_sell = 0
        self.buy_price = 0
        self.sell_price = 0
        self.stop_loss = 0
        self.take_profit = 0

    def close_pos(self, date):
        self.n = 1
        self.notionals.append(self.n * self.opening)
        self.trades.append((self.sell_price-self.buy_price)*self.n - 2*self.n*self.fee)
        self.unit_trades.append(self.trades[-1]/self.n)
        self.account = self.account + self.trades[-1]
        self.account_history.append(self.account)
        self.pnl.append(self.pnl[-1] + self.trades[-1])
        self.dates.append(date)
        self.buy_prices.append(self.buy_price)
        self.sell_prices.append(self.sell_price)

# Getting the dataset Nasdaq 100 Index
stock = yf.Ticker('QQQ')
df = stock.history(period='max', interval='5m')

# Data cleaning
df.reset_index(inplace=True)
print(df.info())

df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True).dt.tz_convert('US/Eastern').dt.tz_localize(None)
print(df.head())

df['day'] = df['Datetime'].dt.date
df['time'] = df['Datetime'].dt.time

df_copy = df.copy()

traderone = Trader()

for t in tqdm(range(1, len(df))):
    pass