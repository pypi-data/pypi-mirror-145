"""
engine/portfolio.py에서 사용되는 MIN_TRADE_AMOUNT를 전 종목에 대하여 생성한 후 pkl파일로 저장하는 스크립트
"""
import os
import time
import pickle
from source.binance_api import BinanceAPI

DIRNAME, _ = os.path.split(os.path.abspath(__file__))


if __name__ == "__main__":
    api = BinanceAPI()

    spot_all_tickers = api.client.get_all_tickers()
    spot_tickers = [d["symbol"] for d in spot_all_tickers if d["symbol"][-4:] == "USDT"]

    futures_all_tickers = api.client.futures_ticker()
    futures_tickers = [d["symbol"] for d in futures_all_tickers]

    # spot / usdt futures에 모두 존재하는 티커 set으로 만들기
    tickers = list(set(spot_tickers).intersection(set(futures_tickers)))

    MIN_TRADE_AMOUNT = {"binance": {"usdt": {}, "margin": {}},
                        "bybit": {"usdt": {"BCHUSDT": {"min_trade_amount": 0.01, "min_digit": 2},
                                           "BTCUSDT": {"min_trade_amount": 0.001, "min_digit": 3},
                                           "ETHUSDT": {"min_trade_amount": 0.01, "min_digit": 2},
                                           "LINKUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "LTCUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "XTZUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "DOTUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "ADAUSDT": {"min_trade_amount": 1, "min_digit": 0},
                                           "UNIUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                            # Newly Added
                                           "BNBUSDT": {"min_trade_amount": 0.01, "min_digit": 2},
                                           "DOGEUSDT": {"min_trade_amount": 1, "min_digit": 0},
                                           "XRPUSDT": {"min_trade_amount": 1, "min_digit": 0},
                                           "SOLUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "MATICUSDT": {"min_trade_amount": 1, "min_digit": 0},
                                           "ETCUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "FILUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "EOSUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "AAVEUSDT": {"min_trade_amount": 0.01, "min_digit": 2},
                                           "SUSHIUSDT": {"min_trade_amount": 0.1, "min_digit": 1},
                                           "XEMUSDT": {"min_trade_amount": 1, "min_digit": 0}}}}

    futures_info_dict = api.client.futures_exchange_info()["symbols"]

    cnt = 1

    for ticker in tickers:
        # MARGIN
        margin_info = api.client.get_symbol_info(symbol=ticker)
        margin_info = margin_info["filters"]
        lot_size = [d for d in margin_info if d["filterType"] == "LOT_SIZE"][0]
        min_trade_amount = lot_size["minQty"]
        min_trade_amount = min_trade_amount.rstrip("0")
        if "." in min_trade_amount:
            amount_str = min_trade_amount.split(".")[1]
            min_trade_amount = float(min_trade_amount)
            min_digit = len(amount_str)
        else:
            min_trade_amount = int(min_trade_amount)
            min_digit = 0
        MIN_TRADE_AMOUNT["binance"]["margin"][ticker] = {"min_trade_amount": min_trade_amount,
                                                         "min_digit": min_digit}
        time.sleep(0.3)

        # USDT FUTURES
        futures_info = [d for d in futures_info_dict if d["symbol"] == ticker][0]["filters"]
        lot_size = [d for d in futures_info if d["filterType"] == "LOT_SIZE"][0]
        min_trade_amount = lot_size["minQty"]
        min_trade_amount = min_trade_amount.rstrip("0")
        if "." in min_trade_amount:
            amount_str = min_trade_amount.split(".")[1]
            min_trade_amount = float(min_trade_amount)
            min_digit = len(amount_str)
        else:
            min_trade_amount = int(min_trade_amount)
            min_digit = 0
        MIN_TRADE_AMOUNT["binance"]["usdt"][ticker] = {"min_trade_amount": min_trade_amount,
                                                       "min_digit": min_digit}
        time.sleep(0.3)

        print(f'[{cnt}/{len(tickers)}] Request for {ticker} SUCCESS')
        cnt += 1

    with open(f"{DIRNAME}\\min_trade_amount.pkl", "wb") as f:
        pickle.dump(MIN_TRADE_AMOUNT, f)