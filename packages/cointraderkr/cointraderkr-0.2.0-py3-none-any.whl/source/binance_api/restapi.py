import os
import time
import datetime
import traceback
import pandas as pd
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

load_dotenv(override=True)

BINANCE_PUBLIC_KEY = os.getenv('YG_BINANCE_PUBLIC_KEY')
BINANCE_SECRET_KEY = os.getenv('YG_BINANCE_SECRET_KEY')


class BinanceAsset:
    SPOT = 'MAIN'
    MARGIN = 'MARGIN'
    ISOLATED_MARGIN = 'ISOLATED_MARGIN'
    USDT_FUTURES = 'UMFUTURE'
    COINM_FUTURES = 'CMFUTURE'


class BinanceAPI:

    COINM_FUTURES_URL = 'https://dapi.binance.com/dapi'
    COINM_FUTURES_API_VERSION = 'v1'

    def __init__(self,
                 public_key=BINANCE_PUBLIC_KEY,
                 secret_key=BINANCE_SECRET_KEY):

        self.client = Client(public_key, secret_key)

        # Isolated Margin Account 자동으로 계정 만들어주기
        try:
            self.existing_isolated_margin_accs = []

            isolated_margin_acc = self.get_isolated_margin_account()
            for info in isolated_margin_acc['assets']:
                self.existing_isolated_margin_accs.append(f"{info['baseAsset']['asset']}USDT")
        except:
            traceback.print_exc()

    def _create_coinm_futures_api_uri(self, path):
        return self.COINM_FUTURES_URL + '/' + self.COINM_FUTURES_API_VERSION + '/' + path

    def _request_coinm_futures_api(self, method, path, signed=False, **kwargs):
        uri = self._create_coinm_futures_api_uri(path)
        return self.client._request(method, uri, signed, True, **kwargs)

    def get_all_tickers(self):
        return self.client.get_all_tickers()

    def get_spot_data(self,
                      symbol: str,
                      interval: str,
                      start_str: str = datetime.datetime.now().strftime('%d %b, %Y'),
                      end_str: str = None):
        """
        :param symbol: BTCUSDT
        :param interval: 1m, 3m, 5m, 10m, 15m, 1h, 4h, 1d
        :param start_str: 1 Dec, 2017
        :param end_str: 1 Jan, 2018
        :return: pd.DataFrame
        """
        columns = [
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Can be ignored'
        ]
        df = pd.DataFrame(self.client.get_historical_klines(symbol=symbol,
                                                            interval=interval,
                                                            start_str=start_str,
                                                            end_str=end_str,
                                                            limit=1000))
        df.columns = columns
        df['Open time'] = df['Open time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        df['Close time'] = df['Close time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        return df

    def get_usdt_futures_data(self,
                              symbol: str,
                              interval: str,
                              start_str: str = datetime.datetime.now().strftime('%d %b, %Y'),
                              end_str: str = None):
        columns = [
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Can be ignored'
        ]
        params = {
            'symbol': symbol,
            'interval': interval,
            'start_str': start_str,
            'end_str': end_str,
            'limit': 1000
        }
        data = self.client._request_futures_api('get', 'klines', True, data=params)
        df = pd.DataFrame(data)
        df.columns = columns
        df['Open time'] = df['Open time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        df['Close time'] = df['Close time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        return df

    def get_coinm_funding_rate_data(self,
                                    symbol: str,
                                    start_str: str = None,
                                    end_str: str = datetime.datetime.now().strftime('%d %b, %Y'),
                                    limit: int = 1000):
        params = {
            'symbol': symbol,
            'limit': limit
        }
        if start_str is not None:
            params['startTime'] = start_str
        if end_str is not None:
            params['endTime'] = end_str
        data = self._request_coinm_futures_api('get', 'fundingRate', True, data=params)
        return data

    ##################
    # Asset Transfer #
    ##################
    def transfer_account(self, from_wallet, to_wallet, asset, amount):
        transfer_type = f'{from_wallet}_{to_wallet}'
        params = {
            'type': transfer_type,
            'asset': asset,
            'amount': amount
        }
        return self.client._request_margin_api('post', 'asset/transfer', signed=True, data=params)

    def transfer_isolated_margin_account(self, from_wallet, to_wallet, asset, symbol, amount):
        """
        isolated margin account는 transfer하기 위한 함수가 따로 존재한다.
        """
        params = {
            'asset': asset,
            'symbol': symbol,
            'transFrom': from_wallet,
            'transTo': to_wallet,
            'amount': amount
        }
        return self.client._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def get_isolated_margin_account_transfer_history(self, **params):
        return self.client._request_margin_api('get', 'margin/isolated/transfer', signed=True, data=params)

    ###################
    # Account Related #
    ###################
    def get_account(self, asset_type, balance_only=False):
        if asset_type == BinanceAsset.SPOT:
            acc = self.client.get_account()
            if balance_only:
                return {d['asset']: d for d in acc['balances']}
            else:
                return acc

        if asset_type == BinanceAsset.MARGIN:
            acc = self.client.get_margin_account()
            if balance_only:
                balance = {'totalAssetOfBtc': acc['totalAssetOfBtc'], 'totalNetAssetOfBtc': acc['totalNetAssetOfBtc']}
                balance['assets'] = {d['asset']: d for d in acc['userAssets']}
                return balance
            else:
                return acc

        if asset_type == BinanceAsset.ISOLATED_MARGIN:
            acc = self.get_isolated_margin_account()
            return acc

        if asset_type == BinanceAsset.USDT_FUTURES:
            acc = self.get_usdt_futures_account()
            return acc

        if asset_type == BinanceAsset.COINM_FUTURES:
            acc = self.get_coinm_futures_account()
            return acc

    ## 일단 급해서 만듬, 추후 get_account 함수에 isolated 조회기능도 추가필요..!
    def get_isolated_margin_account(self, **params):
        res = self.client.get_isolated_margin_account(**params)
        return res

    def create_isolated_margin_account(self, base: str, quote: str):
        """
        :param base: BTC, ETH, ...
        :param quote: USDT
        """
        return self.client.create_isolated_margin_account(**{'base': base, 'quote': quote})

    #### For Account Handler ####
    def get_usdt_futures_account_balance(self, **params):
        return self.client._request_futures_api('get', 'balance', True, data=params)

    def get_usdt_futures_account(self, **params):
        return self.client._request_futures_api('get', 'account', True, data=params)

    def get_coinm_futures_account_balance(self, **params):
        return self._request_coinm_futures_api('get', 'balance', True, data=params)

    def get_coinm_futures_account(self, **params):
        return self._request_coinm_futures_api('get', 'account', True, data=params)

    #################
    # Order Related #
    #################
    def get_spot_orders(self, **params):
        return self.client.get_open_orders(**params)

    def send_spot_order(self, **params):
        return self.client.create_order(**params)

    def cancel_spot_order(self, **params):
        return self.client.cancel_order(**params)

    def send_margin_order(self, **params):
        return self.client.create_margin_order(**params)

    def repay_margin(self, **params):
        return self.client.repay_margin_loan(**params)

    # margin type, leverage를 한번에 수정하는 함수
    def change_usdt_futures_margin_leverage(self, symbol, margin_type, leverage):
        # Try Except로 거를 시 margin_type과 leverage를 바꿔줄 필요가 없는 경우 아무런 msg를 보내지 못함
        # 따라서 매번 request를 보내 조회하여 검증 과정을 한번 거친 후 change 진행.

        if self.get_usdt_futures_margin_type(symbol=symbol)[0]['marginType'].upper() in [margin_type, 'CROSS']:
            margin_type_confirmed = True
        else:
            margin_type_confirmed = False
            self.change_usdt_futures_margin_type(symbol=symbol, marginType=margin_type)

        if self.get_usdt_futures_leverage()[symbol] == leverage:
            leverage_confirmed = True
        else:
            leverage_confirmed = False
            self.change_usdt_futures_leverage(symbol=symbol, leverage=leverage)

        return margin_type_confirmed, leverage_confirmed

    def change_coinm_futures_margin_leverage(self, symbol, margin_type, leverage):
        self.change_coinm_futures_margin_type(symbol=symbol, marginType=margin_type)
        self.change_coinm_futures_leverage(symbol=symbol, leverage=leverage)

    def change_usdt_futures_leverage(self, symbol, leverage):
        params = {'symbol': symbol, 'leverage': leverage}

        try:
            return self.client._request_futures_api('post', 'leverage', True, data=params)
        except:
            traceback.print_exc()

    def get_usdt_futures_leverage(self):
        positions = self.get_usdt_futures_account()['positions']
        return {d['symbol']: int(d['leverage']) for d in positions}

    def change_coinm_futures_leverage(self, symbol, leverage):
        params = {'symbol': symbol, 'leverage': leverage}
        try:
            return self._request_coinm_futures_api('post', 'leverage', True, data=params)
        except:
            traceback.print_exc()

    def get_coinm_futures_leverage(self):
        positions = self.get_coinm_futures_account()['positions']
        return {d['symbol']: int(d['leverage']) for d in positions}

    def change_usdt_futures_margin_type(self, **params):
        return self.client._request_futures_api('post', 'marginType', True, data=params)

    def get_usdt_futures_margin_type(self, **params):
        return self.client._request_futures_api('get', 'positionRisk', True, data=params)

    def change_coinm_futures_margin_type(self, **params):
        return self._request_coinm_futures_api('post', 'marginType', True, data=params)

    def get_coinm_futures_margin_type(self, **params):
        return self._request_coinm_futures_api('get', 'positionRisk', True, data=params)

    def get_usdt_futures_orders(self, **params):
        return self.client._request_futures_api('get', 'openOrders', True, data=params)

    def send_usdt_futures_order(self, **params):
        return self.client._request_futures_api('post', 'order', True, data=params)

    def cancel_usdt_futures_order(self, **params):
        return self.client._request_futures_api('delete', 'order', True, data=params)

    def get_coinm_futures_orders(self, **params):
        return self._request_coinm_futures_api('get', 'openOrders', True, data=params)

    def send_coinm_futures_order(self, **params):
        return self._request_coinm_futures_api('post', 'order', True, data=params)

    def cancel_coinm_futures_order(self, **params):
        return self._request_coinm_futures_api('delete', 'order', True, data=params)

    ########################
    # Market Order Related #
    ########################
    def send_spot_market_order(self, symbol, side, quantity):
        return self.send_spot_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)

    def send_isolated_margin_market_order(self, symbol, side, quantity, sideEffectType):
        return self.send_margin_order(symbol=symbol, isIsolated=True, side=side,
                                      type='MARKET', quantity=quantity, sideEffectType=sideEffectType)

    def send_usdt_futures_market_order(self, symbol, side, quantity):
        return self.send_usdt_futures_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)

    def send_coinm_futures_market_order(self, symbol, side, quantity):
        return self.send_coinm_futures_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)

    ##################
    # Mock Ping Task #
    ##################
    def spot_margin_ping_task(self, monitor_coins: list, amount: float = 0.00000009, sleep: int = 3):
        while True:
            for symbol in monitor_coins:
                self.transfer_isolated_margin_account(from_wallet='SPOT',
                                                      to_wallet='ISOLATED_MARGIN',
                                                      asset='USDT',
                                                      symbol=symbol,
                                                      amount=amount)
                self.transfer_isolated_margin_account(from_wallet='ISOLATED_MARGIN',
                                                      to_wallet='SPOT',
                                                      asset='USDT',
                                                      symbol=symbol,
                                                      amount=amount)
            break
            time.sleep(sleep)

    def usdt_futures_ping_task(self, symbol: str = '1000SHIBUSDT', sleep: int = 3):
        while True:
            try:
                self.change_usdt_futures_margin_type(symbol=symbol, marginType='ISOLATED')
            except BinanceAPIException:
                self.change_usdt_futures_margin_type(symbol=symbol, marginType='CROSSED')
            time.sleep(sleep)

    def coinm_futures_ping_task(self, symbol: str = 'THEATAUSD_PERP', sleep: int = 3):
        while True:
            try:
                self.change_coinm_futures_margin_type(symbol=symbol, marginType='ISOLATED')
            except BinanceAPIException:
                self.change_coinm_futures_margin_type(symbol=symbol, marginType='CROSSED')
            time.sleep(sleep)


if __name__ == '__main__':
    api = BinanceAPI()

    # api.spot_margin_ping_task(['BTCUSDT', 'ETHUSDT'])
    data = api.get_coinm_funding_rate_data('BTCUSD_PERP')
    print(data)

    # while True:
    #     try:
    #         api.change_usdt_futures_margin_type(symbol='1000SHIBUSDT', marginType='ISOLATED')
    #     except BinanceAPIException:
    #         api.change_usdt_futures_margin_type(symbol='1000SHIBUSDT', marginType='CROSSED')
    #     time.sleep(3)

    # api.change_coinm_futures_margin_type(symbol='THETAUSD_PERP', marginType='CROSSED')


    # # changing leverage and margin type
    # api.change_usdt_futures_margin_leverage(symbol='ALICEUSDT',
    #                                         margin_type="ISOLATED",
    #                                         leverage=5)
    # res = api.get_usdt_futures_margin_type(symbol='ALICEUSDT')
    # print(res[0]['marginType'].upper())
    #
    # api.change_usdt_futures_margin_leverage(symbol='ALICEUSDT',
    #                                         margin_type='CROSSED',
    #                                         leverage=1)
    # res = api.get_usdt_futures_margin_type(symbol='ALICEUSDT')
    # print(res[0]['marginType'].upper())



    # res = api.repay_margin(asset='BTC', isIsolated=True, symbol='BTCUSDT', amount=0.00049)
    # pprint(res)

    # acc = api.get_isolated_margin_account(symbol="BTCUSDT")
    # pprint(acc)

    # acc = api.get_account(BinanceAsset.SPOT)
    # print(acc)
    #
    # m_acc = api.get_isolated_account(symbols='BTCUSDT')
    # pprint(m_acc)

    #
    # usdt_acc = api.get_account(BinanceAsset.USDT_FUTURES)
    # print(usdt_acc)
    #
    # coinm_acc = api.get_account(BinanceAsset.COINM_FUTURES)
    # print(coinm_acc)
    #
    #
    # d = api.get_usdt_futures_account_balance()
    # print(d)
    #
    # d = api.get_coinm_futures_account_balance()
    # print(d)

    # lev = api.get_usdt_futures_leverage()
    # print(lev)
    #
    # api.change_usdt_futures_leverage('BTSUSDT', 30)
    #
    # print(api.get_usdt_futures_leverage())
    #
    #
    # print(api.get_spot_orders())

    # # 계좌간 돈 송금 (바이낸스 내에서)
    # res = api.transfer_account(BinanceAsset.SPOT, BinanceAsset.MARGIN, 'USDT', 1)
    #
    # print(res)

    # res = api.transfer_account(BinanceAsset.SPOT, BinanceAsset.USDT_FUTURES, 'USDT', 100)
    # res = api.transfer_account(BinanceAsset.USDT_FUTURES, BinanceAsset.SPOT, 'USDT', 4)
    # res = api.transfer_account(BinanceAsset.COINM_FUTURES, BinanceAsset.SPOT, 'XRP', 0.0223)
    # res = api.transfer_account(BinanceAsset.SPOT, BinanceAsset.COINM_FUTURES, 'BTC', 0.00051985)

    #################################
    # # 크로스 마진 주문 넣고 바로 청산하기
    # res = api.send_margin_order(symbol='BTCUSDT', isIsolated=True, side='BUY',
    #                             type='MARKET', quantity=0.01, sideEffectType='MARGIN_BUY')

    # time.sleep(3)
    #
    # res = api.send_margin_order(symbol='BTCUSDT', isIsolated=True, side='SELL',
    #                             type='MARKET', quantity=0.01, sideEffectType='AUTO_REPAY')
    # #
    # res = api.repay_margin(asset='BTC', isIsolated=True, symbol='BTCUSDT', amount=0.00049)

    # isolated margin 계좌 만들고 주문 넣기
    # res = api.create_isolated_margin_account(base='BTC', quote='USDT')
    # print(res)

    # res = api.transfer_isolated_margin_account(from_type='ISOLATED_MARGIN', to_type='SPOT', asset='USDT', symbol='BTCUSDT', amount=100.0)
    # print(res)

    # acc = api.get_usdt_futures_account()
    # print(acc)

    # lev = api.get_usdt_futures_leverage()
    # print(lev['BTCUSDT'])

    # api.change_usdt_futures_leverage('BTCUSDT', 3)
    #
    # lev = api.get_usdt_futures_leverage()
    # print(lev['BTCUSDT'])
    #
    #
    # r = api.get_usdt_futures_margin_type(symbol='BTCUSDT')
    # print(r)
    #
    # r = api.change_usdt_futures_margin_type(symbol='BTCUSDT', marginType='ISOLATED')
    #
    # r = api.get_usdt_futures_margin_type(symbol='BTCUSDT')
    # print(r)

    # res = api.send_usdt_futures_order(symbol='BTCUSDT', side='SELL', type='MARKET',
    #                                   quantity=0.006)
    #
    # time.sleep(3)
    #
    # res = api.send_usdt_futures_order(symbol='BTCUSDT', side='BUY', type='MARKET',
    #                                   quantity=0.006)
    #
    # print(res)

    # res = api.send_spot_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity='0.005')
    # print(res)

    # res = api.transfer_account(BinanceAsset.SPOT, BinanceAsset.COINM_FUTURES, 'BTC', 0.004995)
    # print(res)

    # lev = api.get_coinm_futures_leverage()
    # print(lev['BTCUSD_PERP'])
    #
    # res = api.change_coinm_futures_leverage('BTCUSD_PERP', 1)
    #
    # lev = api.get_coinm_futures_leverage()
    # print(lev['BTCUSD_PERP'])

    # pos = api.get_coinm_futures_margin_type()
    # print(pos)
    #
    # pos = api.change_coinm_futures_margin_type(symbol='BTCUSD_PERP', marginType='ISOLATED')
    # print(pos)

    # res = api.send_coinm_futures_order(symbol='BTCUSD_PERP', side='SELL', type='MARKET', quantity=2)
    # print(res)

    # res = api.get_usdt_futures_account()
    # print(res)
    #
    # res = api.get_coinm_futures_account()
    # print(res)
    #
    # res = api.get_coinm_futures_account_balance()
    # print(res)