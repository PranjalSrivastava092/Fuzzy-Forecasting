import pandas as pd
import os
from math import sqrt,log
from collections import defaultdict

# print("Stock market prediction system")
# print("Enter the Closing value of market 3 days ago: ")
# cl2 = int(input())
# print("Enter the previous days' Opening Value: ")
# op = int(input())
# print("Closing Value: ")
# cl = int(input())
# print("Highest Value: ")
# hi = int(input())
# print("Lowest Value: ")
# lo = int(input())

#test
cl2 = 20475.73
op = 20461.98
cl = 20307.71
hi = 20470.54
lo = 20383.16


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
		elif(fuzzy_momentum == "SM"):
			return "Bearish"
		elif(fuzzy_momentum == "BG"):
			return "Very Bearish"
		elif(fuzzy_momentum == "VB"):
			return "Extremely Bearish"


def Query(candlestick, trend):
	tf1 = 0
	tf2 = 0
	tf3 = 0
	tf4 = 0
	tf5 = 0
	tf6 = 0
	f1 = open(os.getcwd()+"/documents/fileBL.txt", "r")
	f2 = open(os.getcwd()+"/documents/fileBR.txt", "r")
	f3 = open(os.getcwd()+"/documents/fileNT.txt", "r")

	for x in f1:
		tr, cs = x.strip().split(' ')
		print(cs, candlestick)
		if(tr == trend):
			tf1 = tf1+1
		if(cs == candlestick):
			tf2 = tf2+1


	for x in f2:
		tr, cs = x.split(' ')
		if(tr == trend):
			tf3 = tf3+1
		if(cs == candlestick):
			tf4 = tf4+1


	for x in f3:
		tr, cs = x.split(' ')
		if(tr == trend):
			tf5 = tf5+1
		if(cs == candlestick):
			tf6 = tf6+1
	

	print(tf1, tf2, tf3, tf4, tf5, tf6)
	idf1 = log((298/(1+tf3+tf5)),10)
	idf2 = log((298/(1+tf4+tf6)),10)
	idf3 = log((298/(1+tf1+tf5)),10)
	idf4 = log((298/(1+tf2+tf6)),10)
	idf5 = log((298/(1+tf3+tf1)),10)
	idf6 = log((298/(1+tf2+tf4)),10)

	idf1l = idf1 / sqrt(pow(idf1,2)+pow(idf3,2)+pow(idf5,2))
	idf2l = idf2 / sqrt(pow(idf2,2)+pow(idf4,2)+pow(idf6,2))
	idf3l = idf3 / sqrt(pow(idf1,2)+pow(idf3,2)+pow(idf5,2))
	idf4l = idf4 / sqrt(pow(idf2,2)+pow(idf4,2)+pow(idf6,2))
	idf5l = idf5 / sqrt(pow(idf1,2)+pow(idf3,2)+pow(idf5,2))
	idf6l = idf6 / sqrt(pow(idf2,2)+pow(idf4,2)+pow(idf6,2))
	

	tf1 = 1+log(tf1,10) if (tf1 > 0) else 0 
	tf2 = 1+log(tf2,10) if (tf2 > 0) else 0
	tf3 = 1+log(tf3,10) if (tf3 > 0) else 0
	tf4 = 1+log(tf4,10) if (tf4 > 0) else 0
	tf5 = 1+log(tf5,10) if (tf5 > 0) else 0
	tf6 = 1+log(tf6,10) if (tf6 > 0) else 0

	tf1l = tf1 / sqrt(pow(tf1,2)+pow(tf3,2)+pow(tf5,2))
	tf2l = tf2 / sqrt(pow(tf2,2)+pow(tf4,2)+pow(tf6,2))
	tf3l = tf3 / sqrt(pow(tf1,2)+pow(tf3,2)+pow(tf5,2))
	tf4l = tf4 / sqrt(pow(tf2,2)+pow(tf4,2)+pow(tf6,2))
	tf5l = tf5 / sqrt(pow(tf1,2)+pow(tf3,2)+pow(tf5,2))
	tf6l = tf6 / sqrt(pow(tf2,2)+pow(tf4,2)+pow(tf6,2))

	score1 = tf1l * idf1l + tf2l * idf2l
	score2 = tf3l * idf3l + tf4l * idf4l
	score3 = tf5l * idf5l + tf6l * idf6l

	if(score1 > score3):
		if(score1 > score2):
			return "Bullish"
		else:
			return "Bearish"
	else:
		if(score3 > score2):
			return "Neutral"
		else:
			return "Bearish"



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

sum = 0
for i in range(1,299):
	cluster = clusters[i]
	for i in range(0,5):
		sum = sum + abs(cluster[i][0]['Open'] - cluster[i][0]['Close'])
U = sum / 1490

if(cl2 > cl):
	bias = "negative"
else:
	bias = "positive"

momentum = abs(cl2-cl)
fuzzy_momentum = Fuzzy(momentum, U)
trend = Fuzzy_trend(bias, fuzzy_momentum)
if(trend == "Very Bullish" or trend == "Extremely Bullish" or trend == "Bullish Neutral" or trend == "Bullish"):
	trend = "BL"
elif(trend == "Neutral"):
	trend = "NT"
else: 
	trend = "BR"

#candlestick params
RB = abs(op-cl)
if(op > cl):
	CC = "B"
else:
	CC = "W"

if(CC == 'B'):
	US = hi - op
	LS = cl - lo
else:
	US = hi - cl
	LS = op - lo

rb_fuzzy = Fuzzy(RB, U)
us_fuzzy = Fuzzy(US, U)
ls_fuzzy = Fuzzy(LS, U)

fuzzy_candlestick = rb_fuzzy+us_fuzzy+ls_fuzzy+CC

prediction = Query(fuzzy_candlestick, trend)

print("The market trend is predicted to be "+prediction)


