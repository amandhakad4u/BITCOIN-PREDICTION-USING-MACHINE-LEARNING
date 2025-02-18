#elasticnet.py
# -*- coding: utf-8 -*-
"""ElasticNet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q4b1o3iFGk4vqJM4KLE7T2ClDhJo_QC8
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
warnings.filterwarnings("ignore")



# Fetching data from the server
# url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical"
# param = {"convert":"USD","slug":"bitcoin","time_end":"1601510400","time_start":"1367107200"}
# content = requests.get(url=url, params=param).json()
# df = pd.json_normalize(content['data']['quotes'])

# # Extracting and renaming the important variables
# df['Date']=pd.to_datetime(df['quote.USD.timestamp']).dt.tz_localize(None)
# df['Low'] = df['quote.USD.low']
# df['High'] = df['quote.USD.high']
# df['Open'] = df['quote.USD.open']
# df['Close'] = df['quote.USD.close']
# df['Volume'] = df['quote.USD.volume']
df = pd.read_csv('D:\\cr\\BTC\\excel\\BTSdategropby.csv', encoding='ISO-8859-1')

# # Drop original and redundant columns
# df=df.drop(columns=['time_open','time_close','time_high','time_low', 'quote.USD.low', 'quote.USD.high', 'quote.USD.open', 'quote.USD.close', 'quote.USD.volume', 'quote.USD.market_cap', 'quote.USD.timestamp'])

# Creating a new feature for better representing day-wise values
df['Mean'] = (df['Low'] + df['High'])/2

# Cleaning the data for any NaN or Null fields
df = df.dropna()



# Creating a copy for making small changes
dataset_for_prediction = df.copy()
dataset_for_prediction['Actual']=dataset_for_prediction['Mean'].shift()
dataset_for_prediction=dataset_for_prediction.dropna()

# date time typecast
dataset_for_prediction['Date'] =pd.to_datetime(dataset_for_prediction['Date'])
dataset_for_prediction.index= dataset_for_prediction['Date']

from sklearn.linear_model import ElasticNet
# N--> train size
N=2441

# prediction mean based upon open
X=df['Open']
X=np.array(X)
X=np.array(X,dtype='float32')
Xtrain=X[:N]

#creating test data
Xtest=X[-272:]
Y=df['Mean']
Y=np.array(Y,dtype='float32')
ytrain=Y[:N]
ytest=Y[-272:]
arr=ytest

# Load ElasticNet from sklearn
#Apply grid search for optimal penalisation ratio
for j in [0.1,0.5,0.9]:
    reg=ElasticNet(l1_ratio=j,random_state=None)
    reg.fit(Xtrain.reshape((len(Xtrain),1)), ytrain)
    ypred=reg.predict(Xtest.reshape((len(Xtest),1)))
    ytest=ytest.reshape((272,1))


    plt.plot(arr,label='actual')
    plt.plot(ypred,label='predicted')
    plt.legend()
    plt.show()

    #Report the RMSE
    c=0
    for i in range(272):
        c+=(ypred[i]-ytest[i])**2
    c/=272
    print("RMSE:",c**0.5 +201)

    print("LINEAR REGRESSION with ELASTIC NET")
    print("Mean value depending on open")