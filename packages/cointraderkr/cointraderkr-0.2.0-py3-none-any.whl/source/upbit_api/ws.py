import os
import time
import json
import datetime
import websocket
import threading
from pytz import timezone
from dotenv import load_dotenv
from typing import List, Callable

load_dotenv()

ACCESS_KEY = os.getenv('UPBIT_PUBLIC_KEY')
SECRET_KEY = os.getenv('UPBIT_PRIVATE_KEY')


class UpbitWebsocket:

    url = 'wss://api.upbit.com/websocket/v1'

    def __init__(self,
                 public_key: str = ACCESS_KEY,
                 private_key: str = SECRET_KEY,
                 monitor_coins: List[str] = ['BTC'],
                 callback: Callable = lambda x: x):

        self.public_key = public_key
        self.private_key = private_key

        self.monitor_coins = [s if 'KRW' in s else f'KRW-{s}' for s in monitor_coins]
        self.callback = callback

    def stream_exchange_data(self):
        req = [
            {'ticket': 'trade_orderbook_data'},
            {'type': 'trade', 'codes': self.monitor_coins},
            {'type': 'orderbook', 'codes': self.monitor_coins}
        ]
        self.ws.send(json.dumps(req))

    def _time(self):
        return datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d%H%M%S%f")[:-3]

    def start(self):
        self.__connect()

    def reconnect(self):
        self.exit()
        self.__connect()

    def exit(self):
        self.ws.close()

    def ping(self):
        self.ws.send('PING')

    def _keepalive(self):
        self.ping()

        timer = threading.Timer(2, self._keepalive)
        timer.setDaemon(True)
        timer.start()

    def trade_data_format(self, data: dict):
        tz = timezone('Asia/Seoul')
        dt = datetime.datetime.fromtimestamp(int(data['timestamp']) / 1000, tz)

        local_timestamp = self._time()
        server_timestamp = dt.strftime("%Y%m%d%H%M%S%f")[:-3]
        latency = int(local_timestamp) - int(server_timestamp)

        data.pop('type')
        symbol = data.pop('code').replace('KRW-', '')
        data = {
            'source': 'upbit',
            'asset_type': 'spot',
            'type': 'trade',
            'symbol': symbol,
            'local_timestamp': local_timestamp,
            'server_timestamp': server_timestamp,
            'latency': latency,
            **data
        }
        return data

    def orderbook_data_format(self, data: dict):
        tz = timezone('Asia/Seoul')
        dt = datetime.datetime.fromtimestamp(int(data['timestamp']) / 1000, tz)

        local_timestamp = self._time()
        server_timestamp = dt.strftime("%Y%m%d%H%M%S%f")[:-3]
        latency = int(local_timestamp) - int(server_timestamp)

        data.pop('type')
        symbol = data.pop('code').replace('KRW-', '')

        # 호가 데이터 만들기
        hoga_data = {
            'total_ask_size': data['total_ask_size'],
            'total_bid_size': data['total_bid_size']
        }
        asks_hoga_tmp = {}
        asks_hoga_stack_tmp = {}
        bids_hoga_tmp = {}
        bids_hoga_stack_tmp = {}

        orderbook_units = data.pop('orderbook_units')

        for i, orderbook in enumerate(orderbook_units):
            asks_hoga_tmp[f'sell_hoga{i+1}'] = orderbook['ask_price']
            asks_hoga_stack_tmp[f'sell_hoga{i+1}_stack'] = orderbook['ask_size']
            bids_hoga_tmp[f'buy_hoga{i+1}'] = orderbook['bid_price']
            bids_hoga_stack_tmp[f'buy_hoga{i+1}_stack'] = orderbook['bid_size']

        hoga_data['asks'] = {**asks_hoga_tmp, **asks_hoga_stack_tmp}
        hoga_data['bids'] = {**bids_hoga_tmp, **bids_hoga_stack_tmp}

        data = {
            'source': 'upbit',
            'asset_type': 'spot',
            'type': 'orderbook',
            'symbol': symbol,
            'local_timestamp': local_timestamp,
            'server_timestamp': server_timestamp,
            'latency': latency,
            **hoga_data
        }
        return data

    def __connect(self):
        self.ws = websocket.WebSocketApp(self.url,
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

        self._keepalive()

    def __on_message(self, message):
        data = json.loads(message)

        if data.get('status') == 'UP':
            data = {
                'source': 'upbit',
                'type': 'pong',
                'local_timestamp': self._time(),
                **data
            }

        if data.get('type') == 'trade':
            data = self.trade_data_format(data)

        if data.get('type') == 'orderbook':
            data = self.orderbook_data_format(data)

        self.callback(data)

    def __on_error(self, error):
        print(error)
        raise Exception(error)

    def __on_open(self):
        print('connected')

    def __on_close(self):
        print('closed')


if __name__ == '__main__':
    def print_data(data):
        print(data)

    ws = UpbitWebsocket(monitor_coins=['BTC', 'ETH'], callback=print_data)
    ws.start()

    ws.stream_exchange_data()

    while True:
        pass