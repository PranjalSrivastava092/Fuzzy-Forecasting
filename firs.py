import pandas as pd
import os
from collections import defaultdict

#membership function
def TNYMF(A,U):
	a = U*0.15
	b = U*0.30

	if(A <= a):
		return 1
	elif(A >= b):
		return 0
	else:
		return (b-A)/(b-a)


def VSMF(A,U):
	a = U*0.15
	b = U*0.30
	c = U*0.45

	if(A == b):
		return 1
	elif(A > a and A < b):
		return (A-a)/(b-a)
	elif(A > b and A < c):
		return (c-A)/(c-b)
	else:
		return 0

def SMMF(A,U):
	b = U*0.30
	c = U*0.45
	d = U*0.60

	if(A == c):
		return 1
	elif(A > b and A < c):
		return (A-b)/(c-b)
	elif(A > c and A < d):
		return (d-A)/(d-c)
	else:
		return 0

def BGMF(A,U):
	c = U*0.45
	d = U*0.60
	e = U*0.75

	if(A == d):
		return 1
	elif(A > c and A < d):
		return (A-c)/(d-c)
	elif(A > d and A < e):
		return (e-A)/(e-d)
	else:
		return 0

def VBMF(A,U):
	e = U*0.75
	d = U*0.60

	if(A <= d):
		return 0
	elif(A >= e):
		return 1
	else:
		return (A-d)/(e-d)

def Fuzzy(A,U):
	tny = TNYMF(A,U)
	vs  = VSMF(A,U)
	sm  = SMMF(A,U)
	bg  = BGMF(A,U)
	vb  = VBMF(A,U)

	maxi = max(tny, vs, sm, bg, vb)

	if(maxi == tny):
		return "TNY"
	elif(maxi == vs):
		return "VS"
	elif(maxi == sm):
		return "SM"
	elif(maxi == bg):
		return "BG"
	else:
		return "VB"

def Fuzzy_trend(bias, fuzzy_momentum):
	if(bias == 'positive'):
		if(fuzzy_momentum == "TNY"):
			return "Neutral"
		elif(fuzzy_momentum == "VS"):
			return "Bullish Neutral"
		elif(fuzzy_momentum == "SM"):
			return "Bullish"
		elif(fuzzy_momentum == "BG"):
			return "Very Bullish"
		elif(fuzzy_momentum == "VB"):
			return "Extremely Bullish"
	else:
		if(fuzzy_momentum == "TNY"):
			return "Neutral"
		elif(fuzzy_momentum == "VS"):
			return "Bearish Neutral"
		elif(future_momentum == "SM"):
			return "Bearish"
		elif(fuzzy_momentum == "BG"):
			return "Very Bearish"
		elif(fuzzy_momentum == "VB"):
			return "Extremely Bearish"

# do not touch; ek faltu ka column aa raha tha
data = pd.read_csv("data.csv")
columns = ['Unnamed: 5']
data = data.drop(columns, axis = 1)

#dataframe => dictionary
k = 1
col = ['Date','Open', 'Close', 'High', 'Low']
datasheet = defaultdict(list)
for i,j in data.iterrows():
	d = dict.fromkeys(col, [])
	d['Date'] = j.Date
	d['Open'] = j.Open
	d['Close'] = j.Close
	d['High'] = j.High
	d['Low'] = j.Low
	datasheet[k].append(d)
	k = k+1

#dictionary => clusters
clusters = defaultdict(list)
for object in datasheet:
	x = int((object-1)/5) +1
	clusters[x].append(datasheet[object])

#calculating all the params of candlesticks
for i in range(1,299):
	cluster = clusters[i]
	sum = 0
	for i in range(0,5):
		sum = sum + abs(cluster[i][0]['Open'] - cluster[i][0]['Close'])
	U = sum/5

	candlestick = cluster[2][0]
	first = cluster[0][0]
	last = cluster[4][0]
	#candlestick params
	RB = abs(candlestick['Open'] - candlestick['Close'])
	if(candlestick['Open'] > candlestick['Close']):
		CC = 'B'
	else:
		CC = 'W'

	if(CC == 'B'):
		US = candlestick['High'] - candlestick['Open']
		LS = candlestick['Close'] - candlestick['Low']
	else:
		US = candlestick['High'] - candlestick['Close']
		LS = candlestick['Open'] - candlestick['Low']
	# print(candlestick['Date'], US , LS , RB)

	#fuzzyfying the candlestick
	rb_fuzzy = Fuzzy(RB, U)
	us_fuzzy = Fuzzy(US, U)
	ls_fuzzy = Fuzzy(LS, U)

	fuzzy_candlestick = rb_fuzzy+us_fuzzy+ls_fuzzy+CC

	#previous trend
	if(first['Close'] > candlestick['Close']):
		prev_bias = 'negative'
		prev_momentum = first['Close'] - candlestick['Close']
	else:
		prev_bias = 'positive'
		prev_momentum = candlestick['Close'] - first['Close']

	fuzzy_momentum = Fuzzy(prev_momentum, U)
	prev_trend = Fuzzy_trend(prev_bias, fuzzy_momentum)


	#future trend 
	if(last['Close'] > candlestick['Close']):
		future_bias = 'positive'
		future_momentum = last['Close'] - candlestick['Close']
	else:
		future_bias = 'negative'
		future_momentum = candlestick['Close'] - last['Close']
	
	fuzzy_momentum = Fuzzy(future_momentum, U)
	future_trend = Fuzzy_trend(future_bias, fuzzy_momentum)	

	if(future_trend == "Very Bullish" or future_trend == "Extremely Bullish" or future_trend == "Bullish Neutral" or future_trend == "Bullish"):
		doc = "BL"
	elif(future_trend == "Neutral"):
		doc = "NT"
	else: 
		doc = "BR"


	#creating the document corpus
	filename = os.getcwd()+ "/documents/file"+doc+".txt"
	f = open(filename, "a+")
	f.write("'"+prev_trend + "'' " + fuzzy_candlestick+"\n")
	f.close()




	