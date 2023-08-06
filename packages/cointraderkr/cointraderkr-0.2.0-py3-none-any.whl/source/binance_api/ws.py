import os
import datetime
import threading
import traceback
from pytz import timezone
from functools import partial
from typing import Callable, List

from autobahn.twisted.websocket import connectWS
from twisted.internet import ssl

from binance.client import Client
from binance.websockets import (
    BinanceSocketManager,
    BinanceClientProtocol,
    BinanceClientFactory,
)
from source.binance_api.meta import *
from source.binance_api import MIN_TRADE_AMOUNT

from dotenv import load_dotenv

load_dotenv(override=True)

MONITOR_COINS = sorted(list(MIN_TRADE_AMOUNT['binance']['usdt'].keys()))

MONITOR_COINM_COINS = [
    'BTCUSD'
]

BINANCE_PUBLIC_KEY = os.getenv('PP_BINANCE_PUBLIC_KEY')
BINANCE_SECRET_KEY = os.getenv('PP_BINANCE_SECRET_KEY')


def localize_binance_date_fmt(binance_date):
    """
    바이낸스는 ms까지 데이터를 제공하지 않기 떄문에 local_timestamp와 데이터를 일치시키기 위해서 000을 강제로 붙여준다.
    """
    tz = timezone('Asia/Seoul')
    local_time = datetime.datetime.fromtimestamp(binance_date // 1000, tz)
    time_str = local_time.strftime('%Y%m%d%H%M%S')
    return f'{time_str}000'


class BinanceAsset:
    SPOT = 'MAIN'
    MARGIN = 'MARGIN'
    ISOLATED_MARGIN = 'ISOLATED_MARGIN'
    USDT_FUTURES = 'UMFUTURE'
    COINM_FUTURES = 'CMFUTURE'


class BinanceWebsocket(BinanceSocketManager):

    COINM_FUTURES_URL = 'https://dapi.binance.com/dapi'
    COINM_FUTURES_API_VERSION = 'v1'

    def __init__(self,
                 public_key: str or None = BINANCE_PUBLIC_KEY,
                 secret_key: str or None = BINANCE_SECRET_KEY,
                 callback: Callable = None,
                 monitor_coins: List[str] = []):

        self.client = Client(public_key, secret_key)
        super().__init__(self.client)

        self.callback = callback
        self.monitor_coins = monitor_coins
        self.hoga_data = {}

    # Format 정의(수정)
    def spot_aggtrade_format(self, msg):
        data = {}
        msg = {BINANCE_SPOT_AGGTRADE[key]: val for key, val in msg.items()}
        data['source'] = 'binance'
        data['asset_type'] = 'spot'
        data['local_timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        data['server_timestamp'] = localize_binance_date_fmt(msg['Event_time'])
        latency = int(data['local_timestamp']) - int(data['server_timestamp'])
        data['latency'] = latency
        data = {**data, **msg}
        return data

    def futures_aggtrade_format(self, data):
        tmp_data = {BINANCE_FUT_AGGTRADE[key]: val for key, val in data['data'].items()}
        del data['data']
        data['source'] = 'binance'
        data['asset_type'] = 'usdt'
        data['local_timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        data['server_timestamp'] = localize_binance_date_fmt(tmp_data['Event_time'])
        latency = int(data['local_timestamp']) - int(data['server_timestamp'])
        data['latency'] = latency
        data = {**data, **tmp_data}
        return data

    def coinm_futures_aggtrade_format(self, data):
        tmp_data = {BINANCE_COINM_FUT_AGGTRADE[key]: val for key, val in data['data'].items()}
        del data['data']
        data['source'] = 'binance'
        data['asset_type'] = 'coinm'
        data['local_timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        data['server_timestamp'] = localize_binance_date_fmt(tmp_data['Event_time'])
        latency = int(data['local_timestamp']) - int(data['server_timestamp'])
        data['latency'] = latency
        data = {**data, **tmp_data}
        return data

    def spot_depth_format(self, data):
        symbol = data.get('s')

        if symbol not in self.hoga_data:
            orderbook = self.client.get_order_book(symbol=symbol)
            self.hoga_data[symbol] = orderbook

        # bids
        bids = data['b']
        bids_list = [{'side': 'Buy', 'price': bids[i][0], 'size': bids[i][1]}
                     for i in range(len(bids))]

        # asks
        asks = data['a']
        asks_list = [{'side': 'Sell', 'price': asks[i][0], 'size': asks[i][1]}
                     for i in range(len(asks))]

        bids_asks = bids_list + asks_list

        if data['u'] > self.hoga_data[symbol]['lastUpdateId']:
            for ba in bids_asks:
                bid_ask_type = ba['side']

                if bid_ask_type == 'Buy':
                    side = 'bids'
                else:
                    side = 'asks'

                bid_ask_data = self.hoga_data[symbol][side]

                updated = False

                for i, d in enumerate(bid_ask_data):
                    # delete
                    if float(d[0]) == float(ba['price']) and float(ba['size']) == 0.0:
                        self.hoga_data[symbol][side].pop(i)
                        updated = True

                    # update
                    if float(d[0]) == float(ba['price']) and float(ba['size']) != 0.0:
                        self.hoga_data[symbol][side][i][1] = ba['size']
                        updated = True

                if not updated:
                    # insert
                    self.hoga_data[symbol][side].append([ba['price'], ba['size']])
                    reversed = True if side == 'bids' else False
                    self.hoga_data[symbol][side] = [h for h in sorted(self.hoga_data[symbol][side], key=lambda k: float(k[0]), reverse=reversed)
                                                    if float(h[1]) != 0.0]

            self.hoga_data[symbol]['lastUpdateId'] = data['u']
            if len(self.hoga_data[symbol]['bids']) > 100:
                self.hoga_data[symbol]['bids'] = self.hoga_data[symbol]['bids'][:100]
            if len(self.hoga_data[symbol]['asks']) > 100:
                self.hoga_data[symbol]['asks'] = self.hoga_data[symbol]['asks'][:100]

        buy_hoga = self.hoga_data[symbol]['bids']
        sell_hoga = self.hoga_data[symbol]['asks']

        tmp_data = {}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i in range(25):
            try:
                hoga_tmp[f'buy_hoga{i + 1}'] = float(buy_hoga[i][0])
                hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = float(buy_hoga[i][1])
            except:
                hoga_tmp[f'buy_hoga{i + 1}'] = None
                hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = None

        tmp_data['bids'] = {**hoga_tmp, **hoga_stack_tmp}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i in range(25):
            try:
                hoga_tmp[f'sell_hoga{i + 1}'] = float(sell_hoga[i][0])
                hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = float(sell_hoga[i][1])
            except:
                hoga_tmp[f'sell_hoga{i + 1}'] = None
                hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = None

        tmp_data['asks'] = {**hoga_tmp, **hoga_stack_tmp}

        # latency calculation
        local_timestamp = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        server_timestamp = localize_binance_date_fmt(data['E'])
        latency = int(local_timestamp) - int(server_timestamp)
        latency = latency

        result = {
            'source': 'binance',
            'asset_type': 'spot',
            'local_timestamp': local_timestamp,
            'server_timestamp': server_timestamp,
            'latency': latency,
            'Event_type': 'depthUpdate',
            'Symbol': symbol,
            **tmp_data
        }

        return result

    def futures_depth20_format(self, data):
        tmp_data = {BINANCE_FUT_ORDER_BOOK20[key]: val for key, val in data['data'].items()}
        del data['data']
        data['source'] = 'binance'
        data['asset_type'] = 'usdt'
        data['local_timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        data['server_timestamp'] = localize_binance_date_fmt(tmp_data['Event_time'])
        latency = int(data['local_timestamp']) - int(data['server_timestamp'])
        data['latency'] = latency
        data = {**data, **tmp_data}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i, d in enumerate(data['asks']):
            hoga_tmp[f'sell_hoga{i + 1}'] = float(d[0])
            hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = float(d[1])

        data['asks'] = {**hoga_tmp, **hoga_stack_tmp}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i, d in enumerate(data['bids']):
            hoga_tmp[f'buy_hoga{i + 1}'] = float(d[0])
            hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = float(d[1])

        data['bids'] = {**hoga_tmp, **hoga_stack_tmp}

        return data

    def coinm_futures_depth20_format(self, data):
        tmp_data = {BINANCE_FUT_ORDER_BOOK20.get(key, key): val for key, val in data['data'].items()}
        del data['data']
        data['source'] = 'binance'
        data['asset_type'] = 'coinm'
        data['local_timestamp'] = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
        data['server_timestamp'] = localize_binance_date_fmt(tmp_data['Event_time'])
        latency = int(data['local_timestamp']) - int(data['server_timestamp'])
        data['latency'] = latency
        data = {**data, **tmp_data}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i, d in enumerate(data['asks']):
            hoga_tmp[f'sell_hoga{i + 1}'] = float(d[0])
            hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = float(d[1])

        data['asks'] = {**hoga_tmp, **hoga_stack_tmp}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i, d in enumerate(data['bids']):
            hoga_tmp[f'buy_hoga{i + 1}'] = float(d[0])
            hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = float(d[1])

        data['bids'] = {**hoga_tmp, **hoga_stack_tmp}

        return data

    def spot_exchange_callback(self, msg):
        stream = msg['e']

        if stream == 'aggTrade':
            msg = self.spot_aggtrade_format(msg)
        elif stream == 'depthUpdate':
            msg = self.spot_depth_format(msg)

        self.callback(msg)

    def futures_exchange_callback(self, msg):
        stream = msg['stream']
        msg['asset_type'] = 'usdt'

        if '@aggTrade' in stream:
            msg = self.futures_aggtrade_format(msg)
        elif '@depth20' in stream:
            msg = self.futures_depth20_format(msg)

        self.callback(msg)

    def coinm_futures_exchange_callback(self, msg):
        stream = msg['stream']
        msg['asset_type'] = 'coinm'

        if '@aggTrade' in stream:
            msg = self.coinm_futures_aggtrade_format(msg)
        elif '@depth20' in stream:
            msg = self.coinm_futures_depth20_format(msg)

        self.callback(msg)

    def spot_account_callback(self, msg):
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': 'spot_account',
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }

        self.callback(data)

    def margin_account_callback(self, msg):
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': 'margin_account',
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }

        self.callback(data)

    def isolated_margin_account_callback(self, msg, symbol=None):
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': 'isolated_margin_account',
            'symbol': symbol,
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }

        self.callback(data)

    def usdt_futures_account_callback(self, msg):
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': 'usdt_futures_account',
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }

        self.callback(data)

    def coinm_futures_account_callback(self, msg):
        msg = {BINANCE_WS_FMT_MAPPER.get(msg['e'], {}).get(key, key): val for key, val in msg.items()}
        data = {
            'source': 'binance',
            'type': 'coinm_futures_account',
            'local_timestamp': datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3],
            **msg
        }

        self.callback(data)

    # USDT Futures
    def start_usdt_futures_user_socket(self):
        factory_url = 'wss://fstream.binance.com/ws/' + self.usdt_future_listen_key
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = self.usdt_futures_account_callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()
        self._conns['usdt'] = connectWS(factory, context_factory)
        return 'usdt'

    def update_usdt_futures_listen_key(self):
        """
        30분 주기로 listen key를 업데이트
        """
        listen_key = self._client._request_futures_api('post', 'listenKey')['listenKey']
        self._listen_keys['usdt'] = listen_key
        if listen_key != self.usdt_future_listen_key:
            self.usdt_future_listen_key = listen_key
            self.start_usdt_futures_user_socket()
        self._timers['usdt'] = threading.Timer(60 * 30, self.update_usdt_futures_listen_key)
        self._timers['usdt'].setDaemon(True)
        self._timers['usdt'].start()

    # COINM Futures
    def _create_coinm_futures_api_uri(self, path):
        return self.COINM_FUTURES_URL + '/' + self.COINM_FUTURES_API_VERSION + '/' + path

    def _request_coinm_futures_api(self, method, path, signed=False, **kwargs):
        uri = self._create_coinm_futures_api_uri(path)
        return self.client._request(method, uri, signed, True, **kwargs)

    def _start_coinm_futures_socket(self, path, callback, prefix='stream?streams='):
        factory_url = 'wss://dstream.binance.com/' + prefix + path
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()
        self._conns[path] = connectWS(factory, context_factory)
        return path

    def start_coinm_futures_user_socket(self):
        factory_url = 'wss://dstream.binance.com/ws/' + self.coinm_future_listen_key
        factory = BinanceClientFactory(factory_url)
        factory.protocol = BinanceClientProtocol
        factory.callback = self.coinm_futures_account_callback
        factory.reconnect = True
        context_factory = ssl.ClientContextFactory()
        self._conns['coinm'] = connectWS(factory, context_factory)
        return 'coinm'

    def update_coinm_futures_listen_key(self):
        listen_key = self._request_coinm_futures_api('post', 'listenKey')['listenKey']
        self._listen_keys['coinm'] = listen_key
        if listen_key != self.coinm_future_listen_key:
            self.coinm_future_listen_key = listen_key
            self.start_coinm_futures_user_socket()
        self._timers['coinm'] = threading.Timer(60 * 30, self.update_coinm_futures_listen_key)
        self._timers['coinm'].setDaemon(True)
        self._timers['coinm'].start()

    ##### Final Stream Functions #####
    def stream_spot_exchange_data(self):
        for coin in self.monitor_coins:
            self._start_socket(f'{coin.lower()}@aggTrade', self.spot_exchange_callback)
            self._start_socket(f'{coin.lower()}@depth@1000ms', self.spot_exchange_callback)

    def stream_futures_exchange_data(self):
        for coin in self.monitor_coins:
            self._start_futures_socket(f'{coin.lower()}@aggTrade', self.futures_exchange_callback)
            self._start_futures_socket(f'{coin.lower()}@depth20@500ms', self.futures_exchange_callback)

    def stream_coinm_futures_exchange_data(self):
        for coin in MONITOR_COINM_COINS:
            self._start_coinm_futures_socket(f'{coin.lower()}_perp@aggTrade', self.coinm_futures_exchange_callback)
            self._start_coinm_futures_socket(f'{coin.lower()}_perp@depth20', self.coinm_futures_exchange_callback)

    def stream_spot_margin_account_data(self):
        print('Starting Binance Spot / Margin User Socket')
        self.start_user_socket(callback=self.spot_account_callback)
        self.start_margin_socket(callback=self.margin_account_callback)
        for symbol in self.monitor_coins:
            try:
                self.start_isolated_margin_socket(symbol=symbol,
                                                  callback=partial(self.isolated_margin_account_callback, symbol=symbol))
            except:
                print(f'Isolated margin account for {symbol} does not exist')

    def _start_usdt_futures_account_stream(self):
        self.usdt_future_listen_key = self._client._request_futures_api('post', 'listenKey')['listenKey']
        self.start_usdt_futures_user_socket()
        self.update_usdt_futures_listen_key()

    def stream_usdt_futures_account_data(self):
        print('Starting Binance USDT Future User Socket')
        try:
            self._start_usdt_futures_account_stream()
        except:
            traceback.print_exc()
            self._start_usdt_futures_account_stream()

    def _start_coinm_futures_account_stream(self):
        self.coinm_future_listen_key = self._request_coinm_futures_api('post', 'listenKey')['listenKey']
        self.start_coinm_futures_user_socket()
        self.update_coinm_futures_listen_key()

    def stream_coinm_futures_account_data(self):
        print('Starting Binance COIN-M Future User Socket')
        try:
            self._start_coinm_futures_account_stream()
        except:
            traceback.print_exc()
            self._start_coinm_futures_account_stream()

    def close(self):
        keys = set(self._conns.keys())
        for key in keys:
            self.stop_socket(key)
            self._stop_account_socket(key)
        self._conns = {}



def print_data(data):
    print(data)
    # local_timestamp = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S%f')[:-3]
    # server_timestamp = localize_binance_date_fmt(data['E'])
    # print(local_timestamp, server_timestamp, ' ---> ', int(local_timestamp) - int(server_timestamp))

def start_thread():
    api = BinanceWebsocket(callback=print_data, monitor_coins=['ETHUSDT'])
    api.stream_spot_margin_account_data()
    api.start()


if __name__ == '__main__':
    import sys
    import time

    start_thread()

    # ob = api.client.get_order_book(symbol='BTCUSDT')
    # print(ob)