import pandas as pd
import datetime as dt

# Read data from CSV file
# The data should contain columns ['Date', 'Open', 'High', 'Low', 'Close']

data = pd.read_csv(r'candleData.csv')
data.set_index('Date')
data['Date'] = pd.to_datetime(data['Date'], format="%d-%m-%Y %H:%M")

# Define time range for Open Range breakout. I have taken some default value
rangeStart = dt.time(9, 15)
rangeEnd = dt.time(9, 30)

# Initialize range high and low
high_price = 0
low_price = 10e7

n = len(data)
i = 0

buy = sell = 0
netpnl = 0
pnl = 0
buy_sl = 0
sell_sl = 0
maxpnl = 0
minpnl = 10e7
# 25 Fifteen minute candles in one day.

# Iterating over all candles.
while i < n:
    curr_time = data['Date'].iloc[i].time()
    curr_date = data['Date'].iloc[i].date()
    # Range
    if curr_time < rangeEnd and curr_time >= rangeStart:
        high_price = max(high_price, data['H'].iloc[i])
        low_price = min(low_price, data['L'].iloc[i])
        #print(curr_time, high_price, low_price)
        i += 1
        continue

    # Buy or Sell triggered.
    else:
        # Buy breakout
        if (data['C'].iloc[i] > high_price and buy == 0):
            buy = data['C'].iloc[i]
            buy_sl = data['L'].iloc[i]
            print(curr_date, curr_time, "Buy entry at: ", buy)

        # Sell breakdown
        elif (data['C'].iloc[i] < low_price and sell == 0):
            sell = data['C'].iloc[i]
            sell_sl = data['H'].iloc[i]
            print(curr_date, curr_time, "Sell entry at: ", sell)

    # Exit
    # 1 Closing Time at 15:15 if SL is not hit.
    if curr_time == dt.time(15, 15):
        if (buy):
            pnl = float(data['C'].iloc[i - 1]) - buy
            buy = 0
            print(curr_date, "Closing day with PNL: ", pnl)

        elif (sell):
            pnl = sell - float(data['C'].iloc[i - 1])
            sell = 0
            print(curr_date, "Closing day at PNL: ", pnl)

        i += 1
        high_price = 0
        low_price = 10e7
        netpnl += pnl
        maxpnl = max(maxpnl, pnl)
        minpnl = min(minpnl, pnl)
        continue

    # 2 Buy SL hit.
    if buy and data['C'].iloc[i] < buy_sl:
        pnl = data['C'].iloc[i] - buy
        buy = 0
        while data['Date'].iloc[i].time() != dt.time(15, 15):
            i += 1

        high_price = 0
        low_price = 10e7
        print(curr_date, curr_time, " SL hit. PNL: ", pnl)

        i += 1
        netpnl += pnl
        maxpnl = max(maxpnl, pnl)
        minpnl = min(minpnl, pnl)
        continue

    # 3 Short SL hit.
    if sell and data['C'].iloc[i] > sell_sl:
        pnl = sell - data['C'].iloc[i]
        sell = 0
        while data['Date'].iloc[i].time() != dt.time(15, 15):
            i += 1

        high_price = 0
        low_price = 10e7
        print(curr_date, curr_time, " SL hit. PNL: ", pnl)

        i += 1
        netpnl += pnl
        maxpnl = max(maxpnl, pnl)
        minpnl = min(minpnl, pnl)
        continue
    i += 1

print("Net Profit and Loss for given date range.", netpnl*50)
