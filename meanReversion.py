import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def plotMeanReversion(ticker):
    figure, axis = plt.subplots(2, 2)
    data = yf.Ticker(ticker)
    data = data.history(interval = '1d', period = '3mo')

    indices = [x for x in range(len(data))]

    avgClose = 0

    for index, row in data.Close.iteritems():
        avgClose+=row

    avgClose /= len(data)

    print(avgClose)

    aroc = calculateAROC(data)

    points = []
    for i in range(len(data)):
        points.append(avgClose)

    points = pd.DataFrame(points)
    points.columns = ['Points']
    print(points)

    axis[0,0].plot(indices, points['Points'])
    axis[0,0].plot(indices, data['Close'])
    plt.show()

def calculateAROC(data):
    difference = data.iloc[len(data) - 1].Close - data.iloc[0].Close
    aroc = difference / (len(data))
    return aroc

def calculateMean(data):
    mean = 0
    for index, row in data.Close.iteritems():
        mean+=row
    mean /= len(data)
    return mean

def calculateMeanReversion(ticker):
    returnData = {}
    tickerData = yf.Ticker(ticker)

    data = tickerData.history(interval = '1d', period = '3mo')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    aroc = calculateAROC(data)
    returnData['ThreeMonthAroc'] = aroc

    data = tickerData.history(interval = '1d', period = '1mo')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    aroc = calculateAROC(data)
    returnData['OneMonthAroc'] = aroc

    data = tickerData.history(interval = '1d', period = '5d')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    aroc = calculateAROC(data)
    returnData['FiveDayAroc'] = aroc

    data = tickerData.history(interval = '1d', period = '3mo')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    mean = calculateMean(data)
    returnData['ThreeMonthMean'] = mean

    data = tickerData.history(interval = '1d', period = '1mo')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    mean = calculateMean(data)
    returnData['OneMonthMean'] = mean

    data = tickerData.history(interval = '1d', period = '5d')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    mean = calculateMean(data)
    returnData['FiveDayMean'] = mean

    return(returnData)