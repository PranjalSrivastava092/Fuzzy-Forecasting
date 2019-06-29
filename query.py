print("Stock market prediction system \n")
print("Enter the Closing value of market 3 days ago: ")
cl2 = int(input())
print("Enter the previous days' Opening Value: ")
op = int(input())
print("Closing Value: ")
cl = int(input())
print("Highest Value: ")
hi = int(input())
print("Lowest Value: ")
lo = int(input())



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
		elif(fuzzy_momentum == "VS" or fuzzy_momentum == "SM"):
			return "Bullish Neutral"
		elif(fuzzy_momentum == "BG"):
			return "Very Bullish"
		elif(fuzzy_momentum == "VB"):
			return "Extremely Bullish"
	else:
		if(fuzzy_momentum == "TNY"):
			return "Neutral"
		elif(fuzzy_momentum == "VS" or fuzzy_momentum == "SM"):
			return "Bearish Neutral"
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



