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
    logger.warning(f"limit - {data.json()}")
    close = np.array([float(i[CLOSE]) for i in data.json()])
    return talib.EMA(close, 8)[-1], talib.EMA(close, 21)[-1], close[-1]


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
        logger.info("Iteration Started")
        ema8, ema21, price = getData(URL=URL)
        logger.info(
            f"EMA8 : {ema8}\{lastEma8}, EMA21 : {ema21}\{lastEma21}, PRICE : {price}")
        if ema8 > ema21 and lastEma8 and lastEma8 < lastEma21:
            buyLogic(symbol, price)
        elif ema8 < ema21 and lastEma8 and lastEma8 > lastEma21:
            sellLogic(symbol, price)
        lastEma8, lastEma21 = ema8, ema21
        time.sleep(1*55)


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "15m"
    limit = "25"
    baseUrl = "https://api.binance.com/api/v3/klines"
    URL = f"{baseUrl}?symbol={symbol}&interval={interval}&limit={limit}"
    logger.info("started")
    main(URL)
