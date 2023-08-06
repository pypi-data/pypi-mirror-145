import os
import json
import time
import datetime
import traceback
import threading
import websocket
from pytz import timezone
from dotenv import load_dotenv
from typing import Callable, List
from binance.client import Client

from source.binance_api.meta import BINANCE_WS_FMT_MAPPER

load_dotenv(override=True)

BINANCE_PUBLIC_KEY = os.getenv('PP_BINANCE_PUBLIC_KEY')
BINANCE_SECRET_KEY = os.getenv('PP_BINANCE_SECRET_KEY')


class BinanceWebsocketV2:
    """
    v2는 account 소켓 연결이 주된 목적이며, 주문을 넣고 체결을 확인하고 바로 연결을 끊는 용도로 사용된다.
    그렇기 때문에 listen key를 업데이트할 필요 없다.
    """

    STREAM_URL = 'wss://stream.binance.com:9443'
    USDT_FUTURES_WS_URL = 'wss://fstream.binance.com'
    COINM_FUTURES_WS_URL = 'wss://dstream.binance.com'

    def __init__(self,
                 public_key: str = BINANCE_PUBLIC_KEY,
                 secret_key: str = BINANCE_SECRET_KEY,
                 callback: Callable = None,
                 monitor_coins: List[str] = ['BTCUSDT', 'ETHUSDT', 'ETCUSDT', 'DOGEUSDT'],
                 enable_isolated_margin: bool = False):

        self.client = Client(public_key, secret_key)
        self.callback = callback

        self.url = None
        self.symbol = None
        self.socket_type = None
        self.monitor_coins = monitor_coins

        if enable_isolated_margin:
            for symbol in monitor_coins:
                try:
                    self.enable_isolated_margin_account(symbol)
                except:
                    traceback.print_exc()
                    print(f'Failed to create isolated margin account for: {symbol}')

    def connect(self, url: str):
        self.url = url
        self.__connect(url)

    def exit(self):
        self.ws.close()

    def reconnect(self):
        self.exit()
        self.__connect(self.url)

    def __connect(self, url: str):
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.__on_message,
                                         on_close=self.__on_close,
                                         on_open=self.__on_open,
                                         on_error=self.__on_error,
                                         keep_running=True)

        self.wst = threading.Thread(target=lambda: self.ws.run_forever())
        self.wst.daemon = True
        self.wst.start()

        # Wait for connect before continuing
        retry_times = 5
        while not self.ws.sock or not self.ws.sock.connected and retry_times:
            time.sleep(1)
            retry_times -= 1

        if retry_times == 0 and not self.ws.sock.connected:
            self.reconnect()
            raise websocket.WebSocketTimeoutException('Error！ Could not connect to WebSocket!')

    def __on_message(self, msg: str):
        msg = json.loads(msg)
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': self.socket_type,
            'symbol': self.symbol,
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }
        self.callback(data)

    def __on_error(self, error):
        pass

    def __on_open(self):
        pass

    def __on_close(self):
        pass

    def transfer_isolated_margin_account(self, symbol: str, from_wallet: str, to_wallet: str):
        """
        wallet types: SPOT, ISOLATED_MARGIN
        """
        params = {
            'asset': 'USDT',
            'symbol': symbol,
            'transFrom': from_wallet,
            'transTo': to_wallet,
            'amount': 0.01
        }
        return self.client._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def enable_isolated_margin_account(self, symbol: str):
        self.transfer_isolated_margin_account(symbol, 'SPOT', 'ISOLATED_MARGIN')
        self.transfer_isolated_margin_account(symbol, 'ISOLATED_MARGIN', 'SPOT')
        params = {'symbol': symbol}
        return self.client._request_margin_api('post', 'margin/isolated/account', signed=True, data=params)

    def get_spot_account_listen_key(self):
        return self.client.stream_get_listen_key()

    def get_margin_account_listen_key(self):
        return self.client.margin_stream_get_listen_key()

    def get_isolated_margin_account_listen_key(self, symbol: str):
        return self.client.isolated_margin_stream_get_listen_key(symbol)

    def get_usdt_futures_account_listen_key(self):
        return self.client._request_futures_api('post', 'listenKey')['listenKey']

    def get_coinm_futures_account_listen_key(self):
        pass

    def subscribe_spot_account(self):
        self.socket_type = 'spot_account'
        listen_key = self.get_spot_account_listen_key()
        url = f'{self.STREAM_URL}/ws/{listen_key}'
        self.connect(url)

    def subscribe_margin_account(self):
        self.socket_type = 'margin_account'

    def subscribe_isolated_margin_account(self, symbol: str):
        self.symbol = symbol
        self.socket_type = 'isolated_margin_account'
        listen_key = self.get_isolated_margin_account_listen_key(symbol)
        url = f'{self.STREAM_URL}/ws/{listen_key}'
        self.connect(url)

    def subscribe_usdt_futures_account(self):
        self.socket_type = 'usdt_futures_account'
        listen_key = self.get_usdt_futures_account_listen_key()
        url = f'{self.USDT_FUTURES_WS_URL}/ws/{listen_key}'
        self.connect(url)

    def subscribe_coinm_futures_account(self):
        self.socket_type = 'coinm_futures_account'


class BinanceBulkWebsocket:

    def __init__(self,
                 public_key: str = BINANCE_PUBLIC_KEY,
                 secret_key: str = BINANCE_SECRET_KEY,
                 symbol: str = None,
                 callback: Callable = None):
        self.symbol = symbol
        self.spot_ws = BinanceWebsocketV2(public_key, secret_key, callback)
        self.margin_ws = BinanceWebsocketV2(public_key, secret_key, callback)
        self.usdt_ws = BinanceWebsocketV2(public_key, secret_key, callback)

    def start(self):
        self.spot_ws.subscribe_spot_account()
        self.margin_ws.subscribe_isolated_margin_account(self.symbol)
        self.usdt_ws.subscribe_usdt_futures_account()

    def stop(self):
        self.spot_ws.exit()
        self.margin_ws.exit()
        self.usdt_ws.exit()


if __name__ == '__main__':
    def print_data(data):
        print(data)

    ws = BinanceBulkWebsocket(symbol='ETHUSDT', callback=print_data)
    ws.start()


    while True:
        time.sleep(30)
        break

    ws.stop()