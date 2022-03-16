"""
UNDER CONSTRUCTION

"""


import numpy as np
import websocket as ws
import json
import pandas as pd
import time
import ta

pair = "btcusdt"
time = "1m"
SOCKET = f"wss://stream.binance.com:9443/ws/{pair}@kline_{time}"

df = pd.DataFrame(columns=["open", "high", "low", "close"])
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
        df.loc[len(df)] = [float(open), float(high), float(low), float(close)]
        print(df)


def onClose(wso):
    pass


if __name__ == "__main__":
    a = ws.WebSocketApp(
        SOCKET, on_close=onClose, on_message=onM)
    a.run_forever()
