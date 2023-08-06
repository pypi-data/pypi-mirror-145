import os
import hmac
import json
import time
import socket
import logging
import calendar
import datetime
import traceback
import websocket
import threading
from time import sleep
from pytz import timezone

from dotenv import load_dotenv

load_dotenv(override=True)

hostname = socket.gethostname()
hostnum = os.getenv('HOST_NUM')

# API key를 사용하는 socket 연결이 주기적으로 끊기는 것 같아서
# api key를 2개 사용하여 다른 IP에서 번갈아가며 소켓 연결을 실행하도록 하기
if hostname == 'coin-trader-kr-server-1' or hostnum == '1':
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_SERVER_1_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_SERVER_1_SECRET_KEY')
elif hostname == 'coin-trader-kr-server-2' or hostnum == '2':
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_SERVER_2_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_SERVER_2_SECRET_KEY')
else:
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_SERVER_DEV_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_SERVER_DEV_SECRET_KEY')

URL_MAPPER = {
    'wss://stream.bytick.com/realtime_public': 'usdt',
    'wss://stream.bybit.com/realtime_public': 'usdt',
    'wss://stream.bytick.com/realtime_private': 'usdt',
    'wss://stream.bybit.com/realtime_private': 'usdt',
    'wss://stream.bybit.com/realtime': 'coinm',
    'wss://stream.bytick.com/realtime': 'coinm'
}

def localize_bybit_data_fmt(bybit_ts_data):
    if type(bybit_ts_data) == str and ('T' in bybit_ts_data or 'Z' in bybit_ts_data):
        bybit_ts_data = bybit_ts_data.replace('T', '') \
                                     .replace('Z', '') \
                                     .replace('-', '') \
                                     .replace(':', '') \
                                     .replace('.', '') \
                                     .replace(' ', '')

        # time.mktime이 아닌 calendar.timegm을 사용한다.
        # 차이: time모듈은 로컬 타임을 생성하고, calendar모듈은 UTC 타임을 생성한다.
        bybit_ts_data = calendar.timegm(
            datetime.datetime.strptime(bybit_ts_data, '%Y%m%d%H%M%S%f')
                             .replace(tzinfo=datetime.timezone.utc)
                             .timetuple()
        )
        bybit_ts_data = str(int(bybit_ts_data * 1000000))

    tz = timezone('Asia/Seoul')
    local_time = datetime.datetime.fromtimestamp(int(bybit_ts_data) // 1000000, tz) # microseconds
    time_str = local_time.strftime('%Y%m%d%H%M%S')
    return f'{time_str}000'


class BybitWebsocket:

    def __init__(self, wsURL, api_key=None, api_secret=None, callback=None):
        self.logger = logging.getLogger(__name__)

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')

        self.wsURL = wsURL
        self.asset_type = URL_MAPPER[wsURL]
        self.api_key = api_key
        self.api_secret = api_secret
        self.callback = callback
        self.hoga_data = {}

        self.exited = False
        self.auth = False

        self.__connect(wsURL)

    def _time(self):
        return datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d%H%M%S%f")[:-3]

    def exit(self):
        self.exited = True
        self.ws.close()

    def reconnect(self):
        # reconnect after 2 seconds
        self.exit()
        self.exited = False
        self.__connect(self.wsURL)

    def __connect(self, wsURL):
        self.ws = websocket.WebSocketApp(wsURL,
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
            sleep(1)
            retry_times -= 1

        if retry_times == 0 and not self.ws.sock.connected:
            self.reconnect()
            raise websocket.WebSocketTimeoutException('Error！ Could not connect to WebSocket!')

        if self.api_key and self.api_secret:
            self.__do_auth()

    def _make_params(self, op, args=None):
        params = {'op': op}
        if args is not None:
            params['args'] = args
        return params

    def generate_signature(self, expires):
        _val = 'GET/realtime' + expires
        return str(hmac.new(bytes(self.api_secret, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())

    def do_auth(self):
        self.__do_auth()

    def __do_auth(self):
        # 5초: grace period
        expires = str(int(round(time.time()) + 5)) + "000"
        signature = self.generate_signature(expires)
        params = self._make_params('auth', [self.api_key, expires, signature])
        args = json.dumps(params)
        self.ws.send(args)

    def __on_message(self, message):
        data = json.loads(message)
        topic = data.get('topic')

        if topic is not None:
            topics = topic.split('.')
            if set(['position', 'execution', 'order', 'stop_order', 'wallet']) & set(topics):
                asset_type = self.asset_type
            else:
                symbol = topic.split('.')[1]
                if 'USDT' in symbol:
                    asset_type = 'usdt'
                else:
                    asset_type = 'coinm'
            data = self.stream_data_handler(data, asset_type)
        else:
            data = {'source': 'bybit', **data}

        if type(data) == list:
            for d in data:
                self.callback(d)
        else:
            self.callback(data)

    def __on_error(self, error):
        if not self.exited:
            self.logger.error("Error : %s" % error)
            raise websocket.WebSocketException(error)

    def __on_open(self):
        self.logger.debug("Websocket Opened.")

    def __on_close(self):
        self.logger.info('Websocket Closed')

    def update_hoga(self, hoga_data, asset_type, data):
        coin_symbol = data['topic'].split('.')[-1]

        if data['type'] == 'snapshot':
            if asset_type == 'coinm':
                hoga_data[coin_symbol] = data['data']
            else: # usdt
                hoga_data[coin_symbol] = data['data']['order_book']
        elif data['type'] == 'delta' and coin_symbol in hoga_data:
            delete = data['data']['delete']
            update = data['data']['update']
            insert = data['data']['insert']

            if delete:
                for d in delete:
                    for i, h in enumerate(hoga_data[coin_symbol]):
                        if float(d['price']) == float(h['price']):
                            del hoga_data[coin_symbol][i]

            if update:
                for d in update:
                    for i, h in enumerate(hoga_data[coin_symbol]):
                        if float(d['price']) == float(h['price']):
                            hoga_data[coin_symbol][i]['size'] = float(d['size'])

            if insert:
                for d in insert:
                    hoga_data[coin_symbol].append(d)
                    hoga_data[coin_symbol] = sorted(hoga_data[coin_symbol], key=lambda k: k['price'], reverse=True)

        # sell_hoga: 낮은 가격에서 높은 가격으로 정렬
        # buy_hoga: 높은 가격에서 낮은 가격으로 정렬
        sell_hoga = sorted([h for h in hoga_data[coin_symbol] if h['side'] == 'Sell'], key=lambda k: k['price'])
        buy_hoga = sorted([h for h in hoga_data[coin_symbol] if h['side'] == 'Buy'], key=lambda k: k['price'], reverse=True)

        tmp_data = {}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i in range(25):
            try:
                hoga_tmp[f'buy_hoga{i + 1}'] = float(buy_hoga[i]['price'])
                hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = float(buy_hoga[i]['size'])
            except:
                hoga_tmp[f'buy_hoga{i + 1}'] = None
                hoga_stack_tmp[f'buy_hoga{i + 1}_stack'] = None

        tmp_data['bids'] = {**hoga_tmp, **hoga_stack_tmp}

        hoga_tmp = {}
        hoga_stack_tmp = {}

        for i in range(25):
            try:
                hoga_tmp[f'sell_hoga{i + 1}'] = float(sell_hoga[i]['price'])
                hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = float(sell_hoga[i]['size'])
            except:
                hoga_tmp[f'sell_hoga{i + 1}'] = None
                hoga_stack_tmp[f'sell_hoga{i + 1}_stack'] = None

        tmp_data['asks'] = {**hoga_tmp, **hoga_stack_tmp}

        local_timestamp = self._time()
        server_timestamp = localize_bybit_data_fmt(data['timestamp_e6'])
        latency = int(local_timestamp) - int(server_timestamp)

        data = {
            'source': 'bybit',
            'asset_type': asset_type,
            'type': 'orderbook',
            'symbol': coin_symbol,
            'local_timestamp': local_timestamp,
            'server_timestamp': server_timestamp,
            'latency': latency,
            **tmp_data
        }

        return data

    def stream_data_handler(self, data, asset_type):
        data_type = data.get('topic', '')

        if 'trade' in data_type:
            d = []
            for dt in data['data']:
                local_timestamp = self._time()
                server_timestamp = localize_bybit_data_fmt(dt['timestamp'])
                latency = int(local_timestamp) - int(server_timestamp)
                dt['topic'] = data['topic']
                d_inst = {
                    'source': 'bybit',
                    'asset_type': asset_type,
                    'type': 'trade',
                    'local_timestamp': local_timestamp,
                    'server_timestamp': server_timestamp,
                    'latency': latency,
                    **dt
                }
                d.append(d_inst)

        elif 'orderBookL2_25' in data_type:
            d = self.update_hoga(self.hoga_data, asset_type, data)

        elif data_type in ['position', 'execution', 'order', 'stop_order', 'wallet']:
            d = {
                'source': 'bybit',
                'asset_type': asset_type,
                'type': data_type,
                'local_timestamp': self._time(),
                **data
            }

        else:
            d = {
                'source': 'bybit',
                'asset_type': asset_type,
                'local_timestamp': self._time(),
                **data
            }

        return d

    def ping(self):
        try:
            params = self._make_params('ping')
            self.ws.send(json.dumps(params))
        except:
            traceback.print_exc()
            print(f'Bybit Websocket Thread Exited With Error: RESTARTING {self.wsURL}')
            self.reconnect()

    def subscribe_kline(self, symbol: str, interval: str):
        if self.is_inverse(symbol):
            topic_name = 'klineV2.' + interval + '.' + symbol
        else:
            topic_name = 'candle.' + interval + '.' + symbol
        params = self._make_params('subscribe', [topic_name])
        self.ws.send(json.dumps(params))

    def subscribe_orderBookL2(self, symbol, level=None):
        if level is None:
            topic = 'orderBookL2_25.' + symbol
        else:
            topic = 'orderBook_{level}.100ms.{symbol}'.format(level=level, symbol=symbol)
        params = self._make_params('subscribe', [topic])
        self.ws.send(json.dumps(params))

    def subscribe_trade(self, symbol: str):
        params = self._make_params('subscribe', [f'trade.{symbol}'])
        self.ws.send(json.dumps(params))

    def subscribe_insurance(self):
        params = self._make_params('subscribe', ['insurance'])
        self.ws.send(json.dumps(params))

    def subscribe_instrument_info(self, symbol):
        params = self._make_params('subscribe', [f'instrument_info.100ms.{symbol}'])
        self.ws.send(json.dumps(params))

    def subscribe_position(self):
        params = self._make_params('subscribe', ['position'])
        self.ws.send(json.dumps(params))

    def subscribe_execution(self):
        params = self._make_params('subscribe', ['execution'])
        self.ws.send(json.dumps(params))

    def subscribe_order(self):
        params = self._make_params('subscribe', ['order'])
        self.ws.send(json.dumps(params))

    def subscribe_stop_order(self):
        params = self._make_params('subscribe', ['stop_order'])
        self.ws.send(json.dumps(params))

    def subscribe_wallet(self):
        params = self._make_params('subscribe', ['wallet'])
        self.ws.send(json.dumps(params))

    @staticmethod
    def is_inverse(symbol):
        if symbol[-1] != 'T':
            return True
        else:
            return False


def ping_loop(socket):
    socket.ping()

    timer = threading.Timer(1, ping_loop, args=(socket,))
    timer.setDaemon(True)
    timer.start()


if __name__ == '__main__':
    from source.bybit_api import bybit_tickers

    monitor_coins = [
        'BTCUSD'
    ]

    def print_market_data(data):
        print(data)

    usdt_market = BybitWebsocket('wss://stream.bytick.com/realtime', None, None,
                                 print_market_data)

    for coin in monitor_coins:
        usdt_market.subscribe_trade(coin)
        # usdt_market.subscribe_orderBookL2(coin)

    # usdt_market.do_auth()
    # usdt_market.subscribe_position()
    # usdt_market.subscribe_execution()
    # usdt_market.subscribe_order()
    # usdt_market.subscribe_stop_order()
    # usdt_market.subscribe_wallet()

    ping_loop(usdt_market)

    while True:
        time.sleep(2)