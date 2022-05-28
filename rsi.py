import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def plot14dayRSI(ticker):
    figure, axis = plt.subplots(2, 2)

    data = calc14dayRSI(ticker)
    axis[0,0].plot(data['Date'], data['RSI'])
    axis[1, 0].plot(data['Date'], data['Gain'])
    plt.show()

def calc14dayRSI(ticker):
    data = yf.Ticker(ticker)
    data = data.history(interval='1d', period='1mo')
    data.index.name = 'Date'
    data.reset_index(inplace=True)
    newDF = data[['Date', 'Close']].copy()
    gainLoss = (newDF.Close.shift(-1) - data.Close).dropna()
    gainLossPercentage = ((newDF.Close.shift(-1) - data.Close)/data.Close).dropna()
    gainLossPercentage = gainLossPercentage.to_frame()
    gainLossPercentage.columns = ['Gain']
    gainLossPercentage['Date'] = data.Date.shift(-1).dropna()
    reindex = ['Date', 'Gain']
    gainLossPercentage = gainLossPercentage.reindex(columns=reindex)

    firstAvgGain = 0
    firstAvgLoss = 0
    for index, row in gainLossPercentage.head(14).iterrows():
        if (row['Gain'] < 0):
            firstAvgLoss += row['Gain']
        else:
            firstAvgGain += row['Gain']

    firstAvgGain /= 14
    firstAvgLoss /= 14

    gainLossPercentage = gainLossPercentage.iloc[14:].reset_index(drop=True)
    avgGains = []
    avgLosses = []

    avgGains.append(firstAvgGain)
    avgLosses.append(firstAvgLoss)


    for i in range(len(gainLossPercentage.index)):
        if (gainLossPercentage['Gain'].iloc[i] < 0):
            firstAvgLoss = ((firstAvgLoss*13) + gainLossPercentage['Gain'].iloc[i])/14
            avgLosses.append(firstAvgLoss)
            firstAvgGain = (firstAvgGain * 13)/14
            avgGains.append(firstAvgGain)
        else:
            firstAvgGain = ((firstAvgGain * 13) + gainLossPercentage['Gain'].iloc[i]) / 14
            avgGains.append(firstAvgGain)
            firstAvgLoss = (firstAvgLoss * 13) / 14
            avgLosses.append(firstAvgLoss)

    gainLossPercentage['Avg Gain'] = pd.DataFrame(avgGains)
    gainLossPercentage['Avg Loss'] = pd.DataFrame(avgLosses)
    gainLossPercentage['RS'] = abs(gainLossPercentage['Avg Gain']/gainLossPercentage['Avg Loss'])
    gainLossPercentage['RSI'] = 100 - (100/(1+gainLossPercentage['RS']))

    return gainLossPercentage

