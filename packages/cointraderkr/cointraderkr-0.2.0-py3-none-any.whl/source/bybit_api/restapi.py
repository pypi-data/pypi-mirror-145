import os
import time
import pytz
import datetime
import pandas as pd
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from BybitAuthenticator import APIKeyAuthenticator

from dotenv import load_dotenv

load_dotenv(override=True)

BYBIT_PUBLIC_KEY = os.getenv('COIN_ARBIT_BYBIT_PUBLIC_KEY')
BYBIT_PRIVATE_KEY = os.getenv('COIN_ARBIT_BYBIT_PRIVATE_KEY')


def apply(self, r):
    r.headers['User-Agent'] = 'Official-SDKs'
    expires = str(int(round(time.time()) - 1)) + '000'
    r.params['timestamp'] = expires
    r.params['api_key'] = self.api_key
    r.params['recv_window'] = 50000
    r.params['sign'] = self.generate_signature(r)
    return r


APIKeyAuthenticator.apply = apply


def bybit(test=True, config=None, api_key=None, api_secret=None):
    if test:
        host = 'https://api-testnet.bybit.com'
    else:
        host = 'https://api.bybit.com'
    if config is None:
        config = {
            'use_models': False,
            'validate_responses': False,
            'also_return_response': True,
            'host': host
        }
    api_key = api_key
    api_secret = api_secret
    spec_uri = host + "/doc/swagger/v_0_2_12.txt"
    if api_key and api_secret:
        request_client = RequestsClient()
        request_client.authenticator = APIKeyAuthenticator(host, api_key, api_secret)
        return SwaggerClient.from_url(spec_uri, config=config, http_client=request_client)
    else:
        return SwaggerClient.from_url(spec_uri, config=config)


class BybitAPI:

    def __init__(self,
                 public_key: str = BYBIT_PUBLIC_KEY,
                 private_key: str = BYBIT_PRIVATE_KEY):

        self.client = bybit(test=False, api_key=public_key, api_secret=private_key)

    def get_usdt_futures_data(self,
                              symbol: str,
                              interval: str,
                              start_str: str = datetime.datetime.now().strftime('%Y%m%d')):

        interval = interval.replace('m', '')
        if len(start_str) == 8:
            from_timestamp = datetime.datetime.strptime(start_str, '%Y%m%d').timestamp()
        else:
            from_timestamp = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp()
        res = self.client.LinearKline.LinearKline_get(symbol=symbol,
                                                      interval=interval,
                                                      **{'from': from_timestamp})
        data = res.result()
        df = pd.DataFrame(data[0]['result'])
        tz = pytz.timezone('Asia/Seoul')
        df['start_at'] = df['start_at'].apply(lambda t: datetime.datetime.fromtimestamp(t, tz))
        df['open_time'] = df['open_time'].apply(lambda t: datetime.datetime.fromtimestamp(t, tz))
        return df

    def get_coinm_futures_data(self,
                              symbol: str,
                              interval: str,
                              start_str: str = datetime.datetime.now().strftime('%Y%m%d')):

        interval = interval.replace('m', '')
        if len(start_str) == 8:
            from_timestamp = datetime.datetime.strptime(start_str, '%Y%m%d').timestamp()
        else:
            from_timestamp = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').timestamp()
        res = self.client.Kline.LinearKline_get(symbol=symbol,
                                                interval=interval,
                                                **{'from': from_timestamp})
        data = res.result()
        df = pd.DataFrame(data[0]['result'])
        tz = pytz.timezone('Asia/Seoul')
        df['start_at'] = df['start_at'].apply(lambda t: datetime.datetime.fromtimestamp(t, tz))
        df['open_time'] = df['open_time'].apply(lambda t: datetime.datetime.fromtimestamp(t, tz))
        return df

    def get_balance(self, symbol=None):
        # 잔고 조회
        # TODO : API Key 만료 에러시 에러뜸 (알려주는 코드 필요)
        res = self.client.Wallet.Wallet_getBalance().result()[0]['result']
        if symbol is None:
            return res
        else:
            return res.get(symbol, {})

    def get_position(self):
        """
        usdt/coinm futures 계좌의 position 정보를 하나의 딕셔너리로 합쳐서 리턴해주는 함수
        """
        coinm_pos = self.client.Positions.Positions_myPosition().result()[0]['result']
        usdt_pos = self.client.LinearPositions.LinearPositions_myPosition().result()[0]['result']
        pos = {}
        for d in [coinm_pos, usdt_pos]:
            for d_dict in d:
                d_data = d_dict['data']
                pos[d_data['symbol']] = d_data
        return pos

    # ORDER FUNCS #
    def get_usdt_futures_positions(self, symbol=None):
        return self.client.LinearPositions.LinearPositions_myPosition(symbol=symbol).result()[0]['result']

    def get_usdt_futures_margin_type(self):
        return self.client.LinearPositions.LinearPositions_myPosition().result()[0]['result']

    def change_usdt_futures_margin_leverage(self, symbol, margin_type, leverage):
        if margin_type == 'CROSSED':
            m_type = False
        elif margin_type == 'ISOLATED':
            m_type = True
        else:
            raise Exception('margin_type should be CROSSED or ISOLATED')

        margin_type_confirmed = False
        leverage_confirmed = False

        res = self.client.LinearPositions.LinearPositions_switchIsolated(
            symbol=symbol, is_isolated=m_type, buy_leverage=leverage, sell_leverage=leverage
        ).result()

        if res[0]['ret_msg'] == 'Isolated not modified': # 'not need to switch to isolate': 갑자기 ret_msg 바뀜;;;
            # print(res)
            ret = self.change_usdt_futures_leverage(symbol, leverage)
            if ret[0]['ret_msg'] == 'leverage not modified': # 'cannot set leverage which is same to the old leverage':
                # print(ret)
                margin_type_confirmed = True
                leverage_confirmed = True
            else:
                margin_type_confirmed = True
        else:
            margin_type_confirmed = False

        return margin_type_confirmed, leverage_confirmed # False, False or True, False 가능. (True, True 는 당연)

    def change_usdt_futures_leverage(self, symbol, leverage):
        return self.client.LinearPositions.LinearPositions_saveLeverage(
            symbol=symbol, buy_leverage=leverage, sell_leverage=leverage).result()

    def send_usdt_futures_order(self, symbol, side, order_type, qty, price=None,
                                reduce_only=False, close_on_trigger=False, time_in_force='GoodTillCancel'):
        """
        side == Sell entry (Sell로 주문 넣어야함) --> close_on_trigger = False
        side == Sell exit (Buy로 주문) --> close_on_trigger = True

        side == Long entry (Buy로 주문) --> close_on_trigger = False
        side == Long exit (Sell로 주문) --> close_on_trigger = True
        """
        side = side.lower().capitalize()
        order_type = order_type.lower().capitalize()
        params = {
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'qty': qty,
            'time_in_force': time_in_force,
            'reduce_only': reduce_only,
            'close_on_trigger': close_on_trigger
        }
        if order_type == 'Limit':
            params['price'] = price
        return self.client.LinearOrder.LinearOrder_new(**params).result()

    def send_usdt_futures_market_order(self, symbol, side, quantity, enter_exit):
        if enter_exit.lower() == 'ENTER'.lower():
            reduce_only = False
            close_on_trigger = False
        elif enter_exit.lower() == 'EXIT'.lower():
            reduce_only = True
            close_on_trigger = True
        params = {
            'symbol': symbol,
            'side': side,
            'order_type': 'Market',
            'qty': quantity,
            'reduce_only': reduce_only,
            'close_on_trigger': close_on_trigger
        }
        return self.send_usdt_futures_order(**params)


if __name__ == '__main__':
    api = BybitAPI()
    # data = api.get_usdt_futures_data('BTCUSDT', '60m')
    # print(data)

    res = api.client.LinearPositions.LinearPositions_myPosition(symbol='BTCUSDT').result()
    print(res)