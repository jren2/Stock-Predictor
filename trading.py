import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
import alpaca_trade_api as tradeapi
from rsi import calc14dayRSI, plot14dayRSI
from meanReversion import calculateMeanReversion, plotMeanReversion
from config import apiKey, endpoint, secretKey

BASE_URL = endpoint
ALPACA_API_KEY = apiKey
ALPACA_SECRET_KEY = secretKey

api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

def printInfo(rsiCurrent, currPrice, meanReversionData):
    print('RSI: ' + str(rsiCurrent))
    print('Current Price: ' + str(currPrice))
    print('5 Day Mean Reversion: ' + str(meanReversionData['FiveDayMean']))
    print('1 Month Mean Reversion: ' + str(meanReversionData['OneMonthMean']))
    print('3 Month Mean Reversion: ' + str(meanReversionData['ThreeMonthMean']))

def evaluateStock(ticker):
    rsiFrame = calc14dayRSI(ticker)
    rsiCurrent = rsiFrame.iloc[len(rsiFrame) - 1].RSI
    meanReversionData = calculateMeanReversion(ticker)
    currPrice = yf.Ticker('goog').history(interval='1m', period='1d')
    currPrice = currPrice.iloc[len(currPrice) - 1].Open.item()

    if (currPrice > meanReversionData['FiveDayMean'] and rsiCurrent >= 70):
        print('Selling: \n Five day mean: ' + str(meanReversionData['FiveDayMean']) + '\nRSI: ' + str(rsiCurrent))
        api.submit_order(ticker, 1, 'sell', 'market', 'day')
        printInfo(rsiCurrent, currPrice, meanReversionData)
    elif (currPrice > meanReversionData['FiveDayMean']):
        # rsiCurrent is lower than 70
        if (rsiCurrent <= 30):
            print('Buying - RSI shows an oversold stock')
            api.submit_order(ticker, 1, 'buy', 'market', 'day')
            printInfo(rsiCurrent, currPrice, meanReversionData)
        else:
            # rsiCurrent is between 30 and 70
            if (rsiCurrent <= 40):
                if (currPrice < meanReversionData['OneMonthMean'] or currPrice < meanReversionData['ThreeMonthMean']):
                    print('Buying - RSI shows fairly oversold stock and Mean shows increase to mean')
                    printInfo(rsiCurrent, currPrice, meanReversionData)
                    api.submit_order(ticker, 1, 'buy', 'market', 'day')
                else:
                    print('doing nothing')
                    printInfo(rsiCurrent, currPrice, meanReversionData)
            elif (rsiCurrent >= 60):
                if (currPrice > meanReversionData['OneMonthMean'] or currPrice > meanReversionData['ThreeMonthMean']):
                    print('Buying - RSI shows fairly undersold stock and Mean shows decrease to mean')
                    api.submit_order(ticker, 1, 'buy', 'market', 'day')
                    printInfo(rsiCurrent, currPrice, meanReversionData)
                else:
                    print('doing nothing')
                    printInfo(rsiCurrent, currPrice, meanReversionData)
            else:
                # RSI shows stable momentum, mean reversion shows decrease to mean
                print('Selling - stable decrease to mean predicted')
                api.submit_order(ticker, 1, 'sell', 'market', 'day')
                printInfo(rsiCurrent, currPrice, meanReversionData)
    elif(rsiCurrent >= 70):
        # RSI says highly undersold
        if (currPrice > meanReversionData['OneMonthMean'] or currPrice > meanReversionData['ThreeMonthMean']):
            print('Selling - RSI predicts highly undersold and mean reversion shows monthly decrease to mean')
            api.submit_order(ticker, 1, 'sell', 'market', 'day')
            printInfo(rsiCurrent, currPrice, meanReversionData)
        else:
            print('Buying - mean reversion highly predicts increase to mean')
            api.submit_order(ticker, 1, 'buy', 'market', 'day')
            printInfo(rsiCurrent, currPrice, meanReversionData)
    else:
        # currPrice < meanReversionData['FiveDayMean'] and rsiCurrent < 70
        if (rsiCurrent <= 35):
            print('Buying - RSI shows oversold stock and mean reversion predicts increase to mean')
            api.submit_order(ticker, 1, 'buy', 'market', 'day')
            printInfo(rsiCurrent, currPrice, meanReversionData)
        else:
            # rsi shows relative stability
            if (currPrice < meanReversionData['OneMonthMean'] or currPrice < meanReversionData['ThreeMonthMean']):
                print('Buying - RSI shows stability and mean reversion indicates increase to mean')
                api.submit_order(ticker, 1, 'buy', 'market', 'day')
                printInfo(rsiCurrent, currPrice, meanReversionData)
            else:
                print('Selling - rsi shows stability and mean reversion indicates decrease to mean')
                api.submit_order(ticker, 1, 'sell', 'market', 'day')
                printInfo(rsiCurrent, currPrice, meanReversionData)

def main():
    tickers = ['GOOG','TSLA','META','MSFT','AMZN','TSM','NVDA','ADBE','ORCL','CSCO','INTC','TXN']

    for ticker in tickers:
        evaluateStock(ticker)

if __name__ == "__main__":
    main()