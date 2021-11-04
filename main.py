from datetime import date, time, tzinfo, timezone, datetime
import datetime
import pytz
import schedule
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime
from datetime import date
from yahoo_fin import stock_info as si
import csv

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


token = open('/home/pi/Desktop/token.txt', 'r').read()

TOKEN = token.replace('\n', '')

today = date.today()

bot = telegram.Bot(TOKEN)


"""

    update: shows you the current price, % change, RSI, EMA death cross 

    macro: sends you world debt values 

    marcrocharts: sends you gini and stuff

    yieldcurves: sends you yield curves


"""

def start(update: Update, context: CallbackContext) -> None:

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    keyboard = [['/updateStocks', '/updateCrypto'],
               ['/macro', '/yieldCurve'],
               ['/info'],]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.sendMessage(update.message.chat_id, text='Hello! Welcome to the Financial Outlook Telegram bot!'
                              ' This bot displays relevant market data as well as broader macroeconomic data', reply_markup=reply_markup)

    update.message.reply_text('Type /updateStocks to see data for stocks'
                              ' Type /updateCrypto to see data for cryptocurrencies'

                              ' Type /macro to see macroeconomic data'
                              ' Type /yieldCurve to see US treasury and Russian Government bond yield curves'
                              ' Type /info for more info. All charts are updated daily.')

    from datetime import datetime
    user = update.message.from_user
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    fullname = "{} {}".format(first_name, last_name)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logfile = [dt_string, chat_id, fullname, username, 'update']

    with open('telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: Start". format(dt_string, first_name, last_name , username, chat_id))



def updateStocks(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    # open csv and manipulate data

    df = pd.read_csv("data/stocks.csv")

    l = ['EURUSD=X', 'RUB=X', 'USDCNY=X', 'CL=F', 'GC=F', 'TSLA', 'PYPL', '^RUT', '^IXIC', '^GSPC']

    # 1) current price 2) pct change 3) EMA above below 4) RSI
    d = {}

    for i in l:
        
        df = pd.read_csv("data/stocks.csv")

        d["LivePrice{}".format(i)] = df[i].iloc[-1]

        df = pd.read_csv("data/pct_change.csv")

        d["pct_Change{}".format(i)] = df[i].iloc[-1]
        
        df = pd.read_csv("data/{}.csv".format(i))
        
        d["EMA_50{}".format(i)] = df['EMA_50'].iloc[-1]
        d["EMA_200{}".format(i)] = df['EMA_200'].iloc[-1]
        d["RSI{}".format(i)] = df['RSI'].iloc[-1]


    l2 = ['Euro', 'Ruble', 'CNYen', 'Brent', 'Gold', 'Tesla', 'Paypal', 'Russel', 'Nasdaq', 'DJI']

    message = ''
    x = 0

    for i in l2:
        # iterate through list l
        s = l[x]
        # current price string 
        current = ('%s: ' % i) + str(round(d['LivePrice{}'.format(s)],2))
        # percent change 
        pct = d['pct_Change{}'.format(s)]
        
        percent = round((100 * pct),2)
        
        
        # percent change string 
        if percent > 0:
            percentChange = ' 🟢' + str(percent) + 'Δ%'
        else: 
            percentChange = ' 🔴' + str(percent) + 'Δ%'
        

        # EMA
        ema50 = round(d['EMA_50{}'.format(s)],2)
        ema200 = round(d['EMA_200{}'.format(s)],2)
        
        #EMA string
        if ema50 > ema200:
            
            EMA = ' EMA trend 📈 '
            
        else: 
            EMA = ' EMA trend 📉 '
        
        #RSI
        rsi = round(d['RSI{}'.format(s)],2)
        
        #RSI string
        if rsi > 70:
            RSI = ' RSI: {}'.format(rsi) + ' 🔥 '
            
        elif rsi < 30:
            RSI = ' RSI: {}'.format(rsi) + ' 💩 '
            
        else:
            RSI = ' RSI: {}'.format(rsi)
            
        
        m = current + percentChange + EMA + RSI + '\n'
        
        message = message + m
        
        x += 1
    
    chat_id = update.message.chat_id

    bot.send_message(chat_id, message)

    update.message.reply_text(
        'Type /info for more info'
        'Type /macro or /yieldCurve for more data'
        )

    from datetime import datetime
    user = update.message.from_user
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    fullname = "{} {}".format(first_name, last_name)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logfile = [dt_string, chat_id, fullname, username, 'update']

    with open('telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: Update". format(dt_string, first_name, last_name , username, chat_id))



def updateCrypto(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    # open csv and manipulate data


    df = pd.read_csv("data/crypto.csv")

    l = ['BTC','ETH','UNI','CRV']

    # 1) current price 2) pct change 3) EMA above below 4) RSI
    d = {}

    for i in l:

        df = pd.read_csv("data/crypto.csv")

        x = i + '_Close'
        
        d["{}_Close".format(i)] = df[x].iloc[-1]

        df = pd.read_csv("data/crypto_pct_change.csv")


        d["{}_pctChange".format(i)] = df[x].iloc[-1]

        df = pd.read_csv("data/{}.csv".format(i))

        d["EMA_50{}".format(i)] = df['EMA_50'].iloc[-1]
        d["EMA_200{}".format(i)] = df['EMA_200'].iloc[-1]
        d["RSI{}".format(i)] = df['RSI'].iloc[-1]

    

    l2 = ['BTC','ETH','UNI','CRV']

    message = ''
    x = 0

    for i in l2:
        
        # iterate through list l
        s = l[x]
        # current price string 
        current = ('%s: ' % i) + str(round(d['{}_Close'.format(i)],2))
        # percent change 
        pct = d['{}_pctChange'.format(s)]

        percent = round((100 * pct),2)


        # percent change string 
        if percent > 0:
            percentChange = ' 🟢' + str(percent) + 'Δ%'
        else: 
            percentChange = ' 🔴' + str(percent) + 'Δ%'


        # EMA
        ema50 = round(d['EMA_50{}'.format(s)],2)
        ema200 = round(d['EMA_200{}'.format(s)],2)

        #EMA string
        if ema50 > ema200:

            EMA = ' EMA trend 📈 '

        else: 
            EMA = ' EMA trend 📉 '

        #RSI
        rsi = round(d['RSI{}'.format(s)],2)

        #RSI string
        if rsi > 70:
            RSI = ' RSI: {}'.format(rsi) + ' 🔥 '

        elif rsi < 30:
            RSI = ' RSI: {}'.format(rsi) + ' 💩 '

        else:
            RSI = ' RSI: {}'.format(rsi)


        m = current + percentChange + EMA + RSI + '\n'

        message = message + m

        x += 1

    
    chat_id = update.message.chat_id

    bot.send_message(chat_id, message)

    update.message.reply_text(
        'Type /info for more info'
        'Type /macro or /yieldCurve for more data'
        )

    from datetime import datetime
    user = update.message.from_user
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    fullname = "{} {}".format(first_name, last_name)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logfile = [dt_string, chat_id, fullname, username, 'update']

    with open('telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: Update". format(dt_string, first_name, last_name , username, chat_id))



def matricies(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('charts/correlationmatrix30.jpeg', 'rb')
    caption = "180 day correlation matrix {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)



def yieldcurve(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('charts/yieldUS.jpeg', 'rb')
    caption = "US Treasury Yield Curve {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('charts/yieldRU.jpeg', 'rb')
    caption = "Russian Government Bond Yield Curve {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)



def macro(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('charts/giniUS.jpeg', 'rb')
    caption = "US Gini Index {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('charts/giniUSlinRegression.jpeg', 'rb')
    caption = "Linear Regression on US Gini Index {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)


def macroStats(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    varListNames = ["USND", "USGDP", "USDR", "USEDR", "ZHND", "ZHGDP", "ZHDR", "ZHEDR", "JPND", "JPGDP", "JPDR", "JPEDR", "DEDR", "DEGDP", "DEDR", "DEEDR", "UKND", "UKGDP", "UKDR", "UKEDR", "RUND", "RUGDP", "RUDR", "RUEDR"]

    d = {}

    # read data and set to variable 
    for i in varListNames:
    
        with open('data/%s.txt' % i, 'r') as file:
            data = file.read().replace('\n', '')
            d[i] = data

    
    message = ''
    for i in varListNames:
    
        name = i
        value = d[i]
    
    
    message += (name + ' ' + value + '\n')
    
    
    chat_id = update.message.chat_id

    bot.send_message(chat_id, message)




def info(update: Update, context: CallbackContext) -> None:
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    update.message.reply_text(
        'This bot was created by Alexander Lee. This bot was designed to be able to run on an ARM cpu. More features are in the works.'
        )

    from datetime import datetime
    user = update.message.from_user
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    fullname = "{} {}".format(first_name, last_name)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    logfile = [dt_string, chat_id, fullname, username, 'update']

    with open('telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: More Info". format(dt_string, first_name, last_name , username, chat_id))



def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")



def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    
    dispatcher.add_handler(CommandHandler("updateStocks", updateStocks))
    dispatcher.add_handler(CommandHandler("updateCrypto", updateCrypto))

    dispatcher.add_handler(CommandHandler("macro", macro))
    dispatcher.add_handler(CommandHandler("macroStats", macroStats))

    dispatcher.add_handler(CommandHandler("matricies", matricies))
    dispatcher.add_handler(CommandHandler("yieldcurve", yieldcurve))

    dispatcher.add_handler(CommandHandler("info", info))


    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
