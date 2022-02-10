"""
UNDER CONSTRUCTION

"""


import numpy as np
import websocket as ws
import json
import pandas as pd
import time
import ta

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

df = pd.DataFrame(columns=["close", "high", "low"])
alreadyIn = False


def onM(wso, msg):
    print("TICK")
    global alreadyIn, df
    jsonData = json.loads(msg)
    candleData = jsonData['k']
    open = candleData['o']
    close = candleData['c']
    high = candleData['h']
    low = candleData['l']
    volume = candleData['v']
    isClosed = candleData['x']
    if isClosed:
        print(f"O {open} H {high} L {low} C {close}")
        df.loc[len(df)] = [float(close), float(high), float(low)]
        print(df)
        if len(df) > 1:
            rsi = ta.momentum.RSIIndicator.rsi(df["close"], window=2)
            print(rsi)
            # if rsi[-1] > 70 and alreadyIn:
            #     print("SELL")
            #     alreadyIn = False
            # elif rsi[-1] < 30 and not alreadyIn:
            #     print("BUY")
            #     alreadyIn = True


def onClose(wso):
    pass


if __name__ == "__main__":
    df = pd.read_csv("./data.csv", index_col=0)
    print(df)
    df["rsi"] = ta.momentum.RSIIndicator(
        close=df["close"], window=2, fillna=False
    ).rsi()
    print(df)
    # a = ws.WebSocketApp(
    #     SOCKET, on_close=onClose, on_message=onM)
    # a.run_forever()
