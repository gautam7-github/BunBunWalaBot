import requests as http
import pandas as pd
import talib
import numpy as np
import time
import logging

logging.basicConfig(filename="logging.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4


def getData(URL: str = None):
    data = http.get(URL)
    close = np.array([float(i[CLOSE]) for i in data.json()])
    return talib.EMA(close, 8)[-1], talib.EMA(close, 8)[-2], talib.EMA(close, 21)[-1], talib.EMA(close, 21)[-2], close[-1]


def buyLogic(symbol, price):
    logger.info("BUY Signal")
    print("buy signal")
    df = pd.read_csv("transac.csv", index_col=0)
    df.loc[len(df)] = ['BUY', symbol, price, time.time()]
    df.to_csv("transac.csv")


def sellLogic(symbol, price):
    logger.info("SELL Signal")
    print("sell signal")
    df = pd.read_csv("transac.csv", index_col=0)
    df.loc[len(df)] = ['SELL', symbol, price, time.time()]
    df.to_csv("transac.csv")


def main(URL: str = None):
    lastEma8, lastEma21, ema8, ema21 = None, None, None, None
    while True:
        try:
            logger.info("Iteration Started")
            ema8, lastEma8, ema21, lastEma21, price = getData(URL=URL)
            logger.info(
                f"EMA8 : {ema8}\{lastEma8}, EMA21 : {ema21}\{lastEma21}, PRICE : {price}")
            if ema8 > ema21:
                if (lastEma8 < lastEma21) and (price > ema8):
                    buyLogic(symbol, price)
            elif ema8 < ema21:
                if (lastEma8 > lastEma21) and (price < ema8):
                    sellLogic(symbol, price)
            lastEma8, lastEma21 = ema8, ema21
            time.sleep(1*30)
        except Exception as e:
            logger.exception(e)
            time.sleep(1*59)


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "1m"
    limit = "100"
    baseUrl = "https://api.binance.com/api/v3/klines"
    URL = f"{baseUrl}?symbol={symbol}&interval={interval}&limit={limit}"
    logger.info("started")
    main(URL)
