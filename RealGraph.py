import matplotlib


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import *


import json
import datetime
import urllib.request as req
from datetime import timezone
import pandas as pd
matplotlib.use("TkAgg")

import yfinance as yf


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


def animate(i,sensitivity):
    print(coin)
    url = "https://poloniex.com/public?command=returnTradeHistory&currencyPair=USDC_{}&start={}"
    date = datetime.datetime.now() - datetime.timedelta(minutes=450)
    date_str = int(date.replace(tzinfo=timezone.utc).timestamp())
    print(url.format(coin,date_str))

    #print(date)
    json_obj = req.urlopen(url.format(coin,date_str))
    data1 = json.load(json_obj)
    data2 = yf.download(tickers='{}-USD'.format(coin), period='3h', interval='1m',index_as_date = True)
    #print(data1)

    df1 = pd.DataFrame(data1)

    #print(df1.head)

    df2 =pd.DataFrame(data2)
    #print(df2.head)
    df2['timestamp'] = pd.to_datetime(df2.index)
    df2['rate'] = pd.to_numeric(df2['Adj Close'])
    df1['timestamp'] = pd.to_datetime(df1['date'])
    df1['rate'] = pd.to_numeric(df1['rate'])
    #print(df2)
    #print(data2)
    b1 = 0
    c1 = 0
    c2 = 0
    time1 = []
    rate1 = []
    time2 = []
    rate2 = []
    for z in df1.index:
        time1.append(df1['timestamp'][z])
        rate1.append(round(float(df1['rate'][z]), 2))
        if(df1['type'][z]=='buy'):
            b1 += 1
        c1 += 1
    for z in df2.index:
        time2.append(z)
        rate2.append(round(float(df2['rate'][z]), 2))
        c2 += 1
    #for col in data2.columns:
      #  print(col)
    #print(c1)
    #print(c2)
    a.clear()
    price1 = rate1[1]
    price2 = rate2[-1]
    lab1 = "Live {} Price : ${}   -{}".format(coin,price1,"poloniex")
    lab2 = "Live {} Price : ${}   -{}".format(coin,price2,"Yahooe finance")
    lab = lab1 + "\n" + lab2
    #print(lab)
    a.plot(time1, rate1,color = 'g' ,label="Poloniex ")
    a.plot(time2, rate2,color = 'r' ,label="Yahoo Finance ")
    a.set_title(label = lab)

    a.legend()
    #avg_vol = float((c1+c2)/2)
    #buy_rate = b1/avg_vol
    price_fin = (max(rate1)+max(rate2))/2
    price_ini = (min(rate1)+min(rate2))/2
    print((price_fin/price_ini))
    #print(avg_vol,buy_rate,price_fin,price_ini)
    if ((price_fin/price_ini)>(1+sensitivity)):
        lol = "Likely to be in a pump scenario"
    else:
        lol = "Unlikely to be in a pump scenario"
    a.text(time1[-10], max(rate1), 'Is there a pump going on: {}'.format(lol), fontsize=15)

class LiveGraph(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Live {} Graph".format(coin), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class RealGraph():
    def __init__(self,coin_name,sensitivity):
        global coin
        coin = coin_name
        app = LiveGraph()
        app.geometry('1280x720')
        print(sensitivity)
        ani = animation.FuncAnimation(f, animate, interval=5000,fargs=(sensitivity,))
        app.mainloop()
