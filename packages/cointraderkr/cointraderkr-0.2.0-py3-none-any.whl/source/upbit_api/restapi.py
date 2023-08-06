import os
import jwt
import uuid
import hashlib
import requests
import datetime
import pandas as pd
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

ACCESS_KEY = os.getenv('UPBIT_PUBLIC_KEY')
SECRET_KEY = os.getenv('UPBIT_PRIVATE_KEY')


class UpbitAPI:

    def __init__(self, public_key: str = ACCESS_KEY, private_key: str = SECRET_KEY):
        self.public_key = public_key
        self.private_key = private_key

    def _payload(self):
        return {
            'access_key': self.public_key,
            'nonce': str(uuid.uuid4())
        }

    def _query(self, query):
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        return query_hash

    def _headers(self, payload):
        jwt_token = jwt.encode(payload, self.private_key)
        auth_token = f'Bearer {jwt_token}'
        headers = {'Authorization': auth_token}
        return headers

    def get_balance(self):
        headers = self._headers(self._payload())
        res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
        portfolio = res.json()
        self.portfolio = {}
        for p in portfolio:
            self.portfolio[p['currency']] = {
                'q': float(p['balance']),
                'p': float(p['avg_buy_price'])
            }
        return self.portfolio

    def get_position(self, symbol: str):
        """
        마켓별 주분 가능 정보

        market: 'KRW-ETH' or 'ETH'
        """
        if 'KRW' not in symbol:
            symbol = f'KRW-{symbol}'

        query = {'market': symbol}
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.get('https://api.upbit.com/v1/orders/chance',
                           params=query, headers=headers)
        res_data = res.json()
        res_data = {
            'bid_fee': float(res_data['bid_fee']), # 매수 수수료 비율
            'ask_fee': float(res_data['ask_fee']), # 매도 수수료 비율
            'maker_bid_fee': float(res_data['maker_bid_fee']),
            'maker_ask_fee': float(res_data['maker_ask_fee']),
            'min_bid_amount': float(res_data['market']['bid']['min_total']), # 최소 매수 금액
            'min_ask_amount': float(res_data['market']['ask']['min_total']), # 최소 매도 금액
            'max_amount': float(res_data['market']['max_total']), # 최대 매수/매도 금액
            'order_status': res_data['market']['state'], # 마켓 운영 상태
            'bid_order_available': float(res_data['bid_account']['balance']), # 매수 주문 가능 수량
            'bid_order_locked': float(res_data['bid_account']['locked']),
            'ask_order_available': float(res_data['ask_account']['balance']), # 매도 주문 가능 수량
            'ask_order_locked': float(res_data['ask_account']['locked'])
        }
        return res_data

    def get_orders(self, symbol: str, order_state: str):
        """
        order_state: wait, watch, done, cancel
        """
        if 'KRW' not in symbol:
            symbol = f'KRW-{symbol}'

        query = {'market': symbol, 'state': order_state}
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.get('https://api.upbit.com/v1/orders',
                           params=query, headers=headers)
        return res.json()

    def get_waiting_orders(self, symbol: str):
        return self.get_orders(symbol, 'wait')

    def get_done_orders(self, symbol: str):
        return self.get_orders(symbol, 'done')

    def send_order(self,
                   symbol: str,
                   side: str,
                   volume: float or None,
                   price: float or None,
                   order_type: str):

        if 'KRW' not in symbol:
            symbol = f'KRW-{symbol}'

        if side.lower() in ['buy', 'sell']:
            if side.lower() == 'buy':
                side = 'bid'
            if side.lower() == 'sell':
                side = 'ask'

        query = {
            'market': symbol,
            'side': side,
            'ord_type': order_type
        }
        if volume is not None:
            query['volume'] = str(volume)
        if price is not None:
            query['price'] = str(price)
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.post('https://api.upbit.com/v1/orders',
                            params=query, headers=headers)
        return res.json()

    def send_market_buy_order(self, symbol: str, amount: float):
        """
        amount: 1BTC당 매도 1호가가 500 KRW 인 경우, 시장가 매수 시 값을 1000으로 세팅하면 2BTC가 매수된다.

        20000만원치 사고 싶으면 20000 넣으면 됨
        """
        return self.send_order(symbol, 'buy', None, amount, 'price')

    def send_market_sell_order(self, symbol: str, volume: float):
        return self.send_order(symbol, 'sell', volume, None, 'market')

    def cancel_order(self, order_id: str):
        query = {'uuid': order_id}
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.delete('https://api.upbit.com/v1/order',
                              params=query, headers=headers)
        return res.json()

    def transfer_coin(self, currency, amount, address):
        query = {
            'currency': currency,
            'amount': amount,
            'address': address
        }
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.post('https://api.upbit.com/v1/withdraws/coin',
                            params=query, headers=headers)
        return res.json()

    def withdraw_krw(self, amount):
        query = {
            'amount': amount
        }
        query_hash = self._query(query)

        payload = {
            **self._payload(),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512'
        }

        headers = self._headers(payload)
        res = requests.post('https://api.upbit.com/v1/withdraws/krw',
                            params=query, headers=headers)
        return res.json()

    def get_market_code(self):
        headers = {'Accept': 'application/json'}
        res = requests.get('https://api.upbit.com/v1/market/all',
                           params={'isDetails': 'false'},
                           headers=headers)
        return res.json()

    def _get_candle_data(self,
                         candle_type: str,
                         symbol: str,
                         date_to: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                         unit: int = 1,
                         count: int = 200):
        """
        candle_type: days, minutes
        """

        if 'KRW' not in symbol:
            symbol = f'KRW-{symbol}'

        idx_cut = count

        headers = {'Accept': 'application/json'}

        data = []
        done = False

        while not done:
            if candle_type == 'days':
                url = f'https://api.upbit.com/v1/candles/{candle_type}'
            else:
                url = f'https://api.upbit.com/v1/candles/{candle_type}/{unit}'

            res = requests.get(url,
                               params={'market': symbol, 'to': date_to, 'count': 200},
                               headers=headers)
            data.extend(res.json())
            date_to = data[-1]['candle_date_time_utc'].replace('T', ' ')
            count -= 200

            if count <= 0:
                done = True

        df = pd.DataFrame(data)
        df = df.iloc[:idx_cut]
        df = df[['candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume']]
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df.index = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S')
        df.drop('date', axis=1, inplace=True)
        df.sort_index(inplace=True)
        return df

    def get_minute_data(self,
                        symbol: str,
                        date_to: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        unit: int = 1,
                        count: int = 200):
        return self._get_candle_data('minutes', symbol, date_to, unit, count)

    def get_day_data(self,
                     symbol: str,
                     date_to: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     unit: int = 1,
                     count: int = 200):
        return self._get_candle_data('days', symbol, date_to, unit, count)

    def get_orderbook(self, symbols: list):
        symbols = [s if 'KRW' in s else f'KRW-{s}' for s in symbols]
        symbols = ','.join(symbols)

        headers = {'Accept': 'application/json'}
        res = requests.get('https://api.upbit.com/v1/orderbook',
                           headers=headers,
                           params={'markets': symbols})

        res_data = res.json()

        data = {}

        for d in res_data:
            symbol = d['market'].replace('KRW-', '')
            data[symbol] = {
                'timestamp': d['timestamp'],
                'total_ask_size': d['total_ask_size'],
                'total_bid_size': d['total_bid_size']
            }

            asks_hoga_tmp = {}
            asks_hoga_stack_tmp = {}
            bids_hoga_tmp = {}
            bids_hoga_stack_tmp = {}

            for i, orderbook in enumerate(d['orderbook_units']):
                asks_hoga_tmp[f'sell_hoga{i+1}'] = orderbook['ask_price']
                asks_hoga_stack_tmp[f'sell_hoga{i+1}_stack'] = orderbook['ask_size']
                bids_hoga_tmp[f'buy_hoga{i+1}'] = orderbook['bid_price']
                bids_hoga_stack_tmp[f'buy_hoga{i+1}_stack'] = orderbook['bid_size']

            data[symbol]['asks'] = {**asks_hoga_tmp, **asks_hoga_stack_tmp}
            data[symbol]['bids'] = {**bids_hoga_tmp, **bids_hoga_stack_tmp}

        return data


if __name__ == '__main__':
    import time

    up = UpbitAPI()

    # data = up.get_minute_data('BTC', unit=15, count=420)
    # print(data)
    #
    # data = up.get_day_data('BTC', count=100)
    # print(data)

    data = up.get_orderbook(['BTC'])
    impossible_bid_price = data['BTC']['bids']['buy_hoga15']
    print(impossible_bid_price)

    res = up.send_order('BTC', 'buy', 0.0005, impossible_bid_price, 'limit')
    print(res)

    time.sleep(1)


    orders = up.get_waiting_orders('BTC')
    print(orders)
    #
    # orderbook = up.get_orderbook(['BTC'])
    # print(orderbook)

    for order in orders:
        res = up.cancel_order(order['uuid'])
        print(res)

    orders = up.get_waiting_orders('BTC')
    print(orders)



    # res = up.send_order('BTC', 'buy', 0.0005, impossible_bid_price, 'limit')
    # print(res)




    # p = up.get_balance()
    # print(p)
    #
    # code = up.get_market_code()
    # print(code)
    #
    # info = up.get_position('BTC')
    # print(info)
    #
    # orders = up.get_orders('BTC', 'wait')
    # print(orders)

    # min = up.get_minute_data('KRW-BTC', '2018-01-01 00:00:00', 1)
    # print(min)
    #
    # daily = up.get_daily_data('KRW-BTC')
    # print(daily[-1])