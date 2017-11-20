import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as spcs
from decimal import Decimal

#Basic coindesk API hook
#Need to convert pastPrices to 2-D Array of Time / Price

def getCurrentPrice():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
    j_obj = json.loads(response.text)
    x = j_obj["bpi"]["USD"]["rate"]
    return Decimal(x.replace(",", ""))

def getPastPrices(months):
    today = datetime.date.today()
    startDate = today - datetime.timedelta(months*365/12)
    endDate = today - datetime.timedelta(1)
    response = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json?start=" + str(startDate) + "&end=" + str(endDate))
    j_obj = json.loads(response.text)
    pastPrices = j_obj["bpi"]
    #2D Array Conversion
    PP_array = []
    #Use i to represent day instead of using actual date
    #actual date is a string and not easy to read on graph
    i = 1
    for key, value in pastPrices.items():
        PP_array.append([i, value])
        i += 1

    #print(PP_array) Need to convert pastPrices to 2-D Array of Time / Price
    data = np.asarray(PP_array)
    X,y = data[:, 0, np.newaxis], data[:, 1, np.newaxis]
    X = X.astype(int)
    return X, y

def linearRegression(X, y):
	values = spcs.mstats.linregress(X, y)
	slope, intercept = values[0], values[1]
	#linearFunc = lambda x: slope * x + intercept
	#y2 = list(map(linearFunc, X))
	#plt.plot(X, y, 'ro')
	#plt.plot(X, y2, 'r--')
	#plt.xlim(0, len(X))
	#plt.show()
	
	return [slope, intercept]

def polynomialRegression(X, y):
    x = []
    Y= []

    for i in range(len(X)):
        x.append(X[i][0])
        Y.append(y[i][0])

    fit = np.polyfit(x, Y, 3)
    fit_fn = np.poly1d(fit)

    #plt.plot(X, y, 'ro', x, fit_fn(x), '--')
    #plt.xlim(0, len(X))
    #plt.show()
    return fit