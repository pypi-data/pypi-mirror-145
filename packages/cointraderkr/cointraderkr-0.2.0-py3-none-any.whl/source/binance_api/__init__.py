import os
import pickle
from pathlib import Path

from source.binance_api.restapi import BinanceAsset, BinanceAPI

# Windows, Linux, Mac 모든 OS에서 directory를 인식할 수 있도록 pathlib 사용
DIRNAME = Path(os.path.dirname(os.path.abspath(__file__)))

def get_min_trade_amount():
    with open(DIRNAME / 'min_trade_amount.pkl', 'rb') as f:
        min_trade_amount = pickle.load(f)
    return min_trade_amount

# Common Variables
MIN_TRADE_AMOUNT = get_min_trade_amount()


if __name__ == '__main__':
    print(DIRNAME)
    print(MIN_TRADE_AMOUNT)