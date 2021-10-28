import pandas as pd
import yfinance as yf
import yahoofinancials

import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import date

import matplotlib.pyplot as plt
import quandl as ql

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression


#####how many days the correlation is looking at
today = date.today()
d = datetime.timedelta(days=30)
start = today - d

def plot_tickers(tickers, start, end, interval, track, log_plot, normalize):
    data_df = yf.download(tickers,
                          start=start,
                          end=end,
                          interval=interval,
                          progress=False)

    # Drop any NaNs (e.g. when comparing SPY to 'BTC-USD')
    data_df = data_df.dropna()

    # normalize df
    if normalize == True:
        data_df = (data_df - data_df.mean()) / data_df.std()
    else:
        pass

    # Plot tickers
    ticker_list = tickers.split(' ')

    for ticker in ticker_list:
        if ticker == 'BTC-USD':  # put BTC on right axis
            ax = data_df[track, ticker].plot(secondary_y=True, figsize=(14, 10), legend=True, logy=log_plot, grid=True)
        else:
            ax = data_df[track, ticker].plot(figsize=(14, 10), legend=True, logy=log_plot, grid=True)

    ax.get_legend().set_bbox_to_anchor((1.3, 1))

    return data_df


def calc_correlation(data_df, track):
    # Get correlation and sort by sum
    sum_corr = data_df[track].corr().sum().sort_values(ascending=True).index.values

    data_df[track][sum_corr].corr()

    # Call the df with the list from summed correlation, sorted ascending.
    plt.figure(figsize=(13, 8))
    ax = sns.heatmap(data_df[track][sum_corr].corr(),
                     annot=True,
                     cmap="Blues")

    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)


#BTC-USD ETH-USD 
tickers = 'EURUSD=X RUB=X CL=F GLD SPY'

# Timeframe
start = '{}'.format(start)
end = '{}'.format(today)

# Time interval: can be 1m, 1h, 1d
interval = '1d'

# key to track: 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'
track = 'Close'

# plot options
log_plot = False
normalize = True

# plot trends
data_df = plot_tickers(tickers, start, end, interval, track, log_plot, normalize)
#plt.savefig('/home/ubuntu/Desktop/TelegramBot/charts/visualcorrelation30.jpeg', dpi=400, bbox_inches='tight')

# calculate and plot correlations
calc_correlation(data_df, track)
plt.savefig('charts/correlationmatrix30.jpeg', dpi=400, bbox_inches='tight')


#### Yield Curves:

yield_ = ql.get("USTREASURY/YIELD")
today = yield_.iloc[-1,:]
month_ago = yield_.iloc[-30,:]
df = pd.concat([today, month_ago], axis=1)
df.columns = ['Today', '1 Month ago']
#plt.style.use('classic')


df.plot(style={'Today': 'ro-', '1 month ago': 'bx--'}
        ,title='US Treasury Yield Curve, %', figsize=(15,10));

plt.savefig('charts/yieldUS.jpeg', dpi=400, bbox_inches='tight')



###### Russian yield curve

dt = datetime.datetime.today()
year = dt.year
month = dt.month
day = dt.day - 1

d = datetime.date(year, month, day)
wd = d.weekday()

if wd == 6:
    day = dt.day - 2


#yield curve CBRF now
url = 'http://www.cbr.ru/eng/hd_base/zcyc_params/zcyc/?UniDbQuery.Posted=True&UniDbQuery.To=%sF%sF%s' % (day, month, year)       

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

index = []
rates = []
x = 1
for i in range(12):
    X = float(soup.findAll('th',{"class":""})[x].decode_contents())
    Y = float(soup.findAll('td',{"class":""})[x].decode_contents())
    
    x+=1
    index.append(X)
    rates.append(Y)
    

print(rates)
print(url)


#yield curve CBRF one month ago
dt = datetime.datetime.today()
year = dt.year
month = dt.month - 1
day = dt.day

d = datetime.date(year, month, day)
wd = d.weekday()

if wd == 6:
    day = dt.day - 2

# one month ago link:
url = 'http://www.cbr.ru/eng/hd_base/zcyc_params/zcyc/?UniDbQuery.Posted=True&UniDbQuery.To=27%2F09%2F2021'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

index = []
rates1 = []
x = 1
for i in range(12):
    X = float(soup.findAll('th',{"class":""})[x].decode_contents())
    Y = float(soup.findAll('td',{"class":""})[x].decode_contents())
    
    x+=1
    index.append(X)
    rates1.append(Y)
    

print(rates1)
print(url)

# Russian bonds have different maturity rates as compared to US Tbonds
index = ["3M0","6MO","9M","1Y","2Y","3Y","5Y","7Y","10Y","15Y","20Y","30Y"]

df = pd.DataFrame(list(zip(index, rates, rates1)),
               columns =['Maturity', 'Today', '1 Month ago'])


df.plot(style={'Today': 'ro-', '1 month ago': 'bx--'}
        ,title='Russian Government Bond Yield Curve, %', figsize=(15,10));


plt.savefig('charts/yieldRU.jpeg', dpi=400, bbox_inches='tight')



##############################
## macro indicators & data


# INTEREST RATES

# Set the URL you want to webscrape from
url = 'https://fred.stlouisfed.org/series/INTDSRUSM193N'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

KeyRateUS = soup.findAll('span',{"class":"series-meta-observation-value"})[0].decode_contents()

print(KeyRateUS)



#m1 MONEY SUPPLY
url = 'https://fred.stlouisfed.org/series/WM1NS'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")


M1moneyUS = soup.findAll('span',{"class":"series-meta-observation-value"})[0].decode_contents()

print(M1moneyUS)


#student debt 
url = 'https://fred.stlouisfed.org/series/SLOAS'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

StudentDebtUS = soup.findAll('span',{"class":"series-meta-observation-value"})[0].decode_contents()

print(StudentDebtUS)



############# Russian indicator

#Key interest rate CBRF
url = 'https://www.cbr.ru/hd_base/KeyRate/'

# Connect to the URL
response = requests.get(url)

# Parse HTML and save to BeautifulSoup object¶
soup = BeautifulSoup(response.text, "html.parser")

KeyRateRU = soup.findAll('td',{"class":""})[1].decode_contents()

print(KeyRateRU)

##### GINI Coefficient

df = pd.read_csv('https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GINIALLRH&scale=left&cosd=1967-01-01&coed=2020-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-01-01&line_index=1&transformation=lin&vintage_date=2021-10-27&revision_date=2021-10-27&nd=1967-01-01')

df = df.set_index('DATE')

df.plot(figsize=(15,10))

plt.savefig('charts/giniUS.jpeg', dpi=400, bbox_inches='tight')

df.to_csv("giniUS.csv")

df = pd.read_csv('giniUS.csv')

df = pd.read_csv('https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GINIALLRH&scale=left&cosd=1967-01-01&coed=2020-01-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-01-01&line_index=1&transformation=lin')

df.drop('DATE', axis='columns', inplace=True)

df.to_csv("giniUS.csv")

pd.read_csv('giniUS.csv')

data = pd.read_csv('giniUS.csv')  # load data set
X = data.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
Y = data.iloc[:, 1].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions

plt.scatter(X, Y)
plt.plot(X, Y_pred, color='red')
plt.savefig('charts/giniUSlinRegression.jpeg', dpi=400, bbox_inches='tight')





#### Debt

driver = webdriver.Chrome()
driver.get('https://www.usdebtclock.org/world-debt-clock.html')

# USA NATIONAL DEBT
USND = driver.find_element_by_xpath('//span[@id="X2a5BWRG"]').text
# USA GDP NOMINAL
USGDP = driver.find_element_by_xpath('//span[@id="X4a79R9BW"]').text
# USA PUBLIC DEBT TO GDP RATIO
USDR = driver.find_element_by_xpath('//span[@id="X3a34729DW"]').text
# USA EXTERNAL DEBT TO GDP
USEDR = driver.find_element_by_xpath('//span[@id="X5a582BYTA"]').text

# CHINA NATIONAL DEBT
ZHND = driver.find_element_by_xpath('//span[@id="M2a0923KLS"]').text
# CHINA GDP NOMINAL
ZHGDP = driver.find_element_by_xpath('//span[@id="M4a951MKWX"]').text
# CHINA PUBLIC DEBT TO GDP RATIO
ZHDR = driver.find_element_by_xpath('//span[@id="M3a3182UUB"]').text
# CHINA EXTERNAL DEBT TO GDP
ZHEDR = driver.find_element_by_xpath('//span[@id="M5a371BYON"]').text

# JAPAN NATIONAL DEBT
JPND = driver.find_element_by_xpath('//span[@id="R2a9163KRX"]').text
# JAPAN GDP NOMINAL
JPGDP = driver.find_element_by_xpath('//span[@id="R4a189MKIK"]').text
# JAPAN PUBLIC DEBT TO GDP RATIO
JPDR = driver.find_element_by_xpath('//span[@id="R3a0202UKB"]').text
# JAPAN EXTERNAL DEBT TO GDP
JPEDR = driver.find_element_by_xpath('//span[@id="R5a672BYLM"]').text

# GERMANY NATIONAL DEBT
DEDR = driver.find_element_by_xpath('//span[@id="E2a8263KGD"]').text
# GERMANY GDP NOMINAL
DEGDP = driver.find_element_by_xpath('//span[@id="E4a59MKOP"]').text
# GERMANY PUBLIC DEBT TO GDP RATIO
DEDR = driver.find_element_by_xpath('//span[@id="E3a6302UMF"]').text
# GERMANY EXTERNAL DEBT TO GDP
DEEDR = driver.find_element_by_xpath('//span[@id="E5a172BYIB"]').text


# UK NATIONAL DEBT
UKND = driver.find_element_by_xpath('//span[@id="H2a6763MKJ"]').text
# UK GDP NOMINAL
UKGDP = driver.find_element_by_xpath('//span[@id="H4a17MKKN"]').text
# UK PUBLIC DEBT TO GDP RATIO
UKDR = driver.find_element_by_xpath('//span[@id="H3a3402ODV"]').text
# UK EXTERNAL DEBT TO GDP
UKEDR = driver.find_element_by_xpath('//span[@id="H5a382BYOL"]').text

# RUSSIA NATIONAL DEBT
RUND = driver.find_element_by_xpath('//span[@id="G2a5723KEC"]').text
# RUSSIA GDP NOMINAL
RUGDP = driver.find_element_by_xpath('//span[@id="G4a411MKMG"]').text
# RUSSIA PUBLIC DEBT TO GDP RATIO
RUDR = driver.find_element_by_xpath('//span[@id="G3a9582UWX"]').text
# RUSSIA EXTERNAL DEBT TO GDP
RUEDR = driver.find_element_by_xpath('//span[@id="G5a491BYOK"]').text


print("USND = " + USND)
print("USGDP = " + USGDP)
print("USDR = " + USDR)
print("USEDR = " + USEDR)

print(RUND)
print(DEDR)
driver.close()

varList = [USND, USGDP, USDR, USEDR, ZHND, ZHGDP, ZHDR, ZHEDR, JPND, JPGDP, JPDR, JPEDR, DEDR, DEGDP, DEDR, DEEDR, UKND, UKGDP, UKDR, UKEDR, RUND, RUGDP, RUDR, RUEDR]
varListNames = ["USND", "USGDP", "USDR", "USEDR", "ZHND", "ZHGDP", "ZHDR", "ZHEDR", "JPND", "JPGDP", "JPDR", "JPEDR", "DEDR", "DEGDP", "DEDR", "DEEDR", "UKND", "UKGDP", "UKDR", "UKEDR", "RUND", "RUGDP", "RUDR", "RUEDR"]

no = 0

for i in varList:
    a = str(i)

    x = varListNames[no]
    
    file = open(('data/%s.txt') % x, 'w')
    file.write(a)
    file.close()

    no += 1



