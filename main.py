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

TOKEN = 'add your telegram token here'

today = date.today()

bot = telegram.Bot(TOKEN)


def start(update: Update, context: CallbackContext) -> None:

    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)

    keyboard = [['/update', '/matricies'],
               ['/yieldcurves', '/info'],
               ['/list'],]

    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.sendMessage(update.message.chat_id, text='Hello! Welcome to the Financial Forecast and Price Prediction Telegram bot!'
                              ' This bot gives daily price correlations and future price predictions of'
                              ' Bitcoin, Ether, Monero, USD/EUR, USD/RUB, PYPL, TSLA, SP500, and the Russel 2000!', reply_markup=reply_markup)

    update.message.reply_text('Type /update to see the latest correlation matricies and price predictions.'
                              ' Type /list to see the list of analyzed assets.'
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



def list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Commands: \n/BTC \n/ETH \n/UNI \n/GOLD \n/OIL  \n/SP500 \n/EUR \n/RUB'
        )


def update(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)


    USND1 = open('data/USND.txt', 'r').read()
    USGDP = open('data/USGDP.txt', 'r').read()
    USDR = open('data/USDR.txt', 'r').read()
    USEDR = open('data/USEDR.txt', 'r').read()

    US = 'US National Debt: %s /n US Nominal GDP: %s /n US Internal Debt to GDP Ratio %s /n US External Debt to GDP Ratio: %s' % (USND1, USGDP, USDR, USEDR)


    chat_id = update.message.chat_id
    dailyupdate = ("▪{}").format(US)
    bot.send_message(chat_id, dailyupdate)

    update.message.reply_text(
        'Type /list to view specific assets'
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

    with open('/home/ubuntu/Desktop/telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: Update". format(dt_string, first_name, last_name , username, chat_id))



def matricies(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/correlationmatrix180.jpeg', 'rb')
    caption = "180 day correlation matrix {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/correlationmatrix30.jpeg', 'rb')
    caption = "30 day correlation matrix {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)


def yieldcurve(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/yield.jpeg', 'rb')
    caption = "Yield Curve {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)


def GOLD(update, context):
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/GOLDforcast.jpeg', 'rb')
    caption = "Gold forcast chart for {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/GOLDtrend.jpeg', 'rb')
    caption = "Gold performance {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/GOLDforcastwithlines.jpeg', 'rb')
    caption = "Gold performance {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    photo = open('/home/ubuntu/Desktop/TelegramBot/charts/GOLDml.jpeg', 'rb')
    caption = "Actual vs Predicted price of ML model {}".format(today)
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id, photo, caption)

    GOLD1 = open('/home/ubuntu/Desktop/TelegramBot/predictions/futurepriceGOLD.txt', 'r').read()
    GOLD2 = open('/home/ubuntu/Desktop/TelegramBot/predictions/meanabsoluteerrorGOLD.txt', 'r').read()
    GOLD3 = open('/home/ubuntu/Desktop/TelegramBot/predictions/buyprofitGOLD.txt', 'r').read()
    GOLD4 = open('/home/ubuntu/Desktop/TelegramBot/predictions/sellprofitGOLD.txt', 'r').read()
    GOLD5 = open('/home/ubuntu/Desktop/TelegramBot/predictions/totalprofitGOLD.txt', 'r').read()
    GOLD6 = open('/home/ubuntu/Desktop/TelegramBot/predictions/profitpertradeGOLD.txt', 'r').read()


    if type(GOLD1) or type(GOLD2) == int or float:
        #calculating Δ%
        ngold = float(GOLD1)
        s = pd.Series([si.get_live_price("GC=F"), ngold])
        s.pct_change()
        normal_sum = s.pct_change()
        normal_sum.at[1]
        dvGOLD = str(round((normal_sum.at[1] * 100), 2))
        #calculating % error
        ngold2 = float(GOLD2)
        e = (ngold2 / ngold) * 100
        eGOLD = '%.2f' % e
        GOLD = 'Predicted price of Gold in 7 days $%s   (Δ%s%%)\n Model Error: %s%% \n Total buy profit: %s\n Total sell profit: %s \n Total profit: %s \n Profit per trade: %s \n' % (GOLD1, dvGOLD, eGOLD, GOLD3, GOLD4, GOLD5, GOLD6)
        chat_id = update.message.chat_id
        bot.send_message(chat_id, GOLD)
    else:
        text = 'Yahoo Finance is missing data for this asset. Could not run prediction model at this time.'
        chat_id = update.message.chat_id
        bot.send_message(chat_id, text)




def info(update: Update, context: CallbackContext) -> None:
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(
        'This bot uses deep learning LSTM models to analyze time series data of asset prices. All charts and predictions are updated daily.'
        ' Type /update to get stock price correlations.')

    update.message.reply_text(
        'This bot was created by Alexander Lee and uses Tensorflow to analyze time series data. (Go to https://www.tensorflow.org to read more)'
        )

    update.message.reply_text(
        'What does it mean when the bot sends "percent error" alongside the price prediction? This is the machine learning model\'s average prediction error when it was training on the historical price data. In machine learning this is called "mean absolute error". Read more about it here: https://en.wikipedia.org/wiki/Mean_absolute_error'
        )

    update.message.reply_text(
        'Type /moreinfo for more information'
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

    with open('/home/ubuntu/Desktop/telegrambotlog.csv', 'a', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(logfile)

    print("{} Name: {} {} Username: {} Chat ID: {} Function: More Info". format(dt_string, first_name, last_name , username, chat_id))


def moreinfo(update: Update, context: CallbackContext) -> None:
    context.bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(
        'If you like this bot please consider helping keeping it up and running! My ETH address: 0xC2e647AD0a1dF0EC67dC26EB39f3fD57171e13Fe\n This bot consumes on average 30w per hour @ 0.087 cents per kWh ~ $3 a month.')

    update.message.reply_text('Disclaimer: This bot is provided for informational '
                              ' and entertainment purposes only. Any price prediction data generated by this bot does not constitute investment advice.'
                              ' If you like this bot, please consider sharing it!')


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
    dispatcher.add_handler(CommandHandler("list", list))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("matricies", matricies))
    dispatcher.add_handler(CommandHandler("yieldcurve", yieldcurve))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("moreinfo", moreinfo))
    dispatcher.add_handler(CommandHandler("GOLD", GOLD))


    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()