from time import sleep
import numpy as np
import pandas as pd
import math
from bs4 import BeautifulSoup
import requests
import datetime
from dateutil import parser
from requests.models import DecodeError
import yfinance
import talib
import yahoo_fin.stock_info as si
from datetime import datetime as dt, timedelta
import os
import sys
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import stockstats
import matplotlib.pyplot as plt

def scrape_earnings_date(ticker):
    # define URL
    curr_url = 'https://finance.yahoo.com/quote/' + ticker
    # send a GET request and check if the request is successful
    response = requests.get(curr_url)
    if response.status_code != 200:
        print('Failure')

    # Parse raw data
    try:
        results = BeautifulSoup(response.content, 'lxml')
        earnings_date = results.find('span', {"data-reactid":"158"})
        earnings_date = earnings_date.get_text()
    except:
        return('cannot gather data')

    return(earnings_date)

def scrape_market_sentiment():
    # define URL
    curr_url = 'https://www.cnbc.com/'
    # send a GET request and check if the request is successful
    response = requests.get(curr_url)
    if response.status_code != 200:
        print('Failure')

    # Parse raw data
    try:
        results = BeautifulSoup(response.text, 'html.parser')
        headline = results.find(class_='MarketsBanner-teaser')
        headline = headline.get_text()
    except:
        return('cannot gather data')

    return(headline)       

def report_email():

    Recipient = "rsipython7898@gmail.com"
    Sender = "rsipython7898@gmail.com"
    sToken = "78uik89lo"
    port = 465
    context = ssl.create_default_context()
    cid = 0
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
            
            my_email = MIMEMultipart('related')
            my_email["Subject"] = "Stock Report " + str(date)

            server.login(Sender, sToken)

            htmlOpen = """\
                <html>
                <head>
                <style>
                .earningDates {
                border: 5px outset red;
                background-color: grey;
                text-align: left;
                }
                </style>
                <style>
                .marketSentiment {
                border: 5px outset red;
                background-color: grey;
                text-align: center;
                }
                </style>
                </head>
            """
            marketSentimentDIVopen = """\
                <div class="marketSentiment">
            """
            earningsDIVopen = """\
                <div class="earningDates">
            """

            msg = htmlOpen + marketSentimentDIVopen + data + market_sentiment + earningsDIVopen + earningDates

            htmlMSG = MIMEText(msg, 'html')

            my_email.attach(htmlMSG)

            #my_email = MIMEText(msg, "html")
            

            for image in imageName:
                
                cid = cid + 1
                imageCID = str(cid)
                imageSRC = '<img src=\"' + 'cid: image' + imageCID + '\">'
                fp = open(image, 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()

                # Define the image's ID as referenced above
                msgImage.add_header(imageSRC, '<image1>')
                my_email.attach(msgImage)

            server.sendmail(Sender, Recipient, my_email.as_string())

def macro_rsi(ticker):
    try:
        #stockData = yfinance.download(ticker,start,end)
        yfinanceTicker = yfinance.Ticker(ticker)
        stockData = yfinanceTicker.history(interval='1d', period="6mo")
        rsi = talib.RSI(stockData["Close"])
        currentRSI = rsi[-1]
        return(currentRSI)
    except ValueError or DecodeError:
        print('cannot compute macroRSI for: ' + str(ticker))

def dmi(ticker):

    ticker_yahoo = yfinance.Ticker(ticker)
    data = ticker_yahoo.history(period='ytd', interval='1d')
    data2 = stockstats.StockDataFrame.retype(data)
    dmiplus = data2.get('pdi')
    dmiminus = data2.get('mdi')
    dmiminus1 = dmiminus[-1]
    dmiminus2 = dmiminus[-2]
    dmiminus3 = dmiminus[-3]
    dmiminus4 = dmiminus[-4]
    dmiminus5 = dmiminus[-5]
    dmiminus6 = dmiminus[-6]
    dmiminus7 = dmiminus[-7]
    dmiminus8 = dmiminus[-8]
    dmiminus9 = dmiminus[-9]
    dmiminus10 = dmiminus[-10]
    dmiminus11 = dmiminus[-11]
    dmiminus12 = dmiminus[-12]
    dmiminus13 = dmiminus[-13]
    dmiminus14 = dmiminus[-14]
    dmiminus15 = dmiminus[-15]
    dmiplus1 = dmiplus[-1]
    dmiplus2 = dmiplus[-2]
    dmiplus3 = dmiplus[-3]
    dmiplus4 = dmiplus[-4]
    dmiplus5 = dmiplus[-5]
    dmiplus6 = dmiplus[-6]
    dmiplus7 = dmiplus[-7]
    dmiplus8 = dmiplus[-8]
    dmiplus9 = dmiplus[-9]
    dmiplus10 = dmiplus[-10]
    dmiplus11 = dmiplus[-11]
    dmiplus12 = dmiplus[-12]
    dmiplus13 = dmiplus[-13]
    dmiplus14 = dmiplus[-14]
    dmiplus15 = dmiplus[-15]

    print(dmiminus[-15], dmiminus[-14], dmiminus[-13], dmiminus[-12], dmiminus[-11], dmiminus[-10], dmiminus[-9], dmiminus[-8], dmiminus[-7], dmiminus[-6], dmiminus[-5], dmiminus[-4], dmiminus[-3], dmiminus[-2], dmiminus[-1])
    print(dmiplus[-15], dmiplus[-14], dmiplus[-13], dmiplus[-12], dmiplus[-11], dmiplus[-10], dmiplus[-9], dmiplus[-8], dmiplus[-7], dmiplus[-6], dmiplus[-5], dmiplus[-4], dmiplus[-3], dmiplus[-2], dmiplus[-1])
    plotName = ticker + ".png"
    plt.plot([dmiminus15,dmiminus14,dmiminus13,dmiminus12,dmiminus11,dmiminus10,dmiminus9,dmiminus8,dmiminus7,dmiminus6,dmiminus5,dmiminus4,dmiminus3,dmiminus2,dmiminus1])
    plt.plot([dmiplus15,dmiplus14,dmiplus13,dmiplus12,dmiplus11,dmiplus10,dmiplus9,dmiplus8,dmiplus7,dmiplus6,dmiplus5,dmiplus4,dmiplus3,dmiplus2,dmiplus1])
    plt.ylabel(ticker)
    plt.savefig(plotName, bbox_inches='tight')
    plt.clf()

stocks = []
tickers = []
earningDates = ""
positiveKeywords = []
negativeKeywords = []
imageName = []
n = 0
p = 0
cid = 100

date = dt.now()
date.day

start = datetime.datetime.now()-datetime.timedelta(days=365)
end = datetime.datetime.now()
hour = datetime.datetime.now()
hour = hour.time()
hour = int(hour.strftime("%H"))

stocks = stocks if len(stocks) > 0 else [
    line.rstrip() for line in open("stocks.txt", "r")]

data = scrape_market_sentiment()

positiveKeywords = positiveKeywords if len(positiveKeywords) > 0 else [
    line.rstrip() for line in open("positive_keywords.txt", "r")]

negativeKeywords = negativeKeywords if len(negativeKeywords) > 0 else [
    line.rstrip() for line in open("negative_keywords.txt", "r")]

for substring in negativeKeywords:
    if substring in data:
        n = n + 1
    else:
        print(substring + " Not found!")
for substring in positiveKeywords:
    if substring in data:
        p = p + 1
    else:
        print(substring + " Not found!")

if n > p:
    market_sentiment = "<br> Market Sentiment: low"
elif p > n : 
    market_sentiment = "<br> Market Sentiment: high"

data = '<br>' + '<h2>' + data + '</h2>'

for ticker in stocks:
    try:
        macroRSI = macro_rsi(ticker)
        earnings = si.get_next_earnings_date(ticker)
        earningsConv = earnings - date
        earningsConv = earningsConv.days
        if macroRSI <= 35:
            dmi(ticker)
            cid = cid + 1
            imageCID = str(cid)
            Name = ticker + ".png"
            imageName.append(Name)
            imageSRC = '<img src=\"' + 'cid: image' + imageCID + '\">'
            earningsDate = '<br>' + '<h3>' + str(ticker) + '</h3>' + imageSRC + '<br>' + 'RSI: ' + str(macroRSI) + '<br>' + 'Days until earnings: ' + str(earningsConv) + '<br>'
            earningDates = earningDates + earningsDate
    except:
        print('failed for: ' + str(ticker))


report_email()   