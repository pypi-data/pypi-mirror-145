import os
from dotenv import load_dotenv

from source.bybit_api import BybitAPI
from source.binance_api import BinanceAPI, BinanceAsset

load_dotenv(override=True)

BYBIT_PUBLIC_KEY = os.getenv('PP_BYBIT_PUBLIC_KEY')
BYBIT_PRIVATE_KEY = os.getenv('PP_BYBIT_PRIVATE_KEY')

BINANCE_PUBLIC_KEY = os.getenv('PP_BINANCE_PUBLIC_KEY')
BINANCE_PRIVATE_KEY = os.getenv('PP_BINANCE_SECRET_KEY')


class CoinAPI:

    def __init__(self,
                 binance_public_key: str = BINANCE_PUBLIC_KEY,
                 binance_private_key: str = BINANCE_PRIVATE_KEY,
                 bybit_public_key: str = BYBIT_PUBLIC_KEY,
                 bybit_private_key: str = BYBIT_PRIVATE_KEY):

        self.binance = BinanceAPI(binance_public_key, binance_private_key)
        self.bybit = BybitAPI(bybit_public_key, bybit_private_key)

    # execution_mode인 경우 사용할 수 있는 함수
    def make_wallet_transfer(self, source, from_wallet, to_wallet, asset, amount, symbol=None):
        if source == 'binance':
            if from_wallet == BinanceAsset.ISOLATED_MARGIN or to_wallet == BinanceAsset.ISOLATED_MARGIN:
                return self.binance.transfer_isolated_margin_account(from_wallet=from_wallet, to_wallet=to_wallet,
                                                                     asset=asset, symbol=symbol, amount=amount)
            else:
                return self.binance.transfer_account(from_wallet=from_wallet, to_wallet=to_wallet, asset=asset, amount=amount)

    def send_spot_market_order(self, source, symbol, side, quantity):
        if source == 'binance':
            self.binance.send_spot_market_order(symbol=symbol, side=side, quantity=quantity)

    def send_isolated_margin_market_order(self, source, symbol, side, quantity, sideEffectType):
        if source == 'binance':
            self.binance.send_isolated_margin_market_order(symbol=symbol, side=side, quantity=quantity, sideEffectType=sideEffectType)

    def send_usdt_futures_market_order(self, source, symbol, side, quantity, enter_exit=None):
        """
        bybit는 enter_exit은 required
        """
        if source == 'binance':
            return self.binance.send_usdt_futures_market_order(symbol=symbol, side=side, quantity=quantity)
        elif source == 'bybit':
            return self.bybit.send_usdt_futures_market_order(symbol=symbol, side=side, quantity=quantity, enter_exit=enter_exit)

    def send_coinm_futures_market_order(self, source, symbol, side, quantity):
        if source == 'binance':
            self.binance.send_coinm_futures_market_order(symbol=symbol, side=side, quantity=quantity)

    def get_usdt_futures_margin_leverage(self, source, symbol):
        if source == 'binance':
            data = self.binance.get_usdt_futures_margin_type()
            data = [d for d in data if d['symbol'] == symbol]
            if data:
                data = data[0]
            else:
                data = {}
            return {'symbol': symbol, 'leverage': data.get('leverage'), 'margin_type': data.get('marginType')}
        elif source == 'bybit':
            data = self.bybit.get_usdt_futures_positions(symbol=symbol)
            if data:
                data = data[0]
            else:
                data = {}
            is_isolated = data.get('is_isolated')
            mt = 'isolated' if is_isolated else 'cross'
            return {'symbol': symbol, 'leverage': data.get('leverage'), 'margin_type': mt}

    def get_coinm_futures_margin_leverage(self, source, symbol):
        if source == 'binance':
            data = self.binance.get_coinm_futures_margin_type()
            data = [d for d in data if d['symbol'] == symbol]
            if data:
                data = data[0]
            else:
                data = {}
            return {'symbol': symbol, 'leverage': data.get('leverage'), 'margin_type': data.get('marginType')}

    def change_usdt_leverage(self, source, symbol, margin_type, leverage):
        if source == 'binance':
            margin_type_confirmed, leverage_confirmed = self.binance.change_usdt_futures_margin_leverage(symbol=symbol, margin_type=margin_type, leverage=leverage)
        elif source == 'bybit':
            margin_type_confirmed, leverage_confirmed = self.bybit.change_usdt_futures_margin_leverage(symbol=symbol, margin_type=margin_type, leverage=leverage)
        else:
            margin_type_confirmed, leverage_confirmed = None, None

        return margin_type_confirmed, leverage_confirmed

    def change_coinm_leverage(self, source, symbol, margin_type, leverage):
        if source == 'binance':
            self.binance.change_coinm_futures_margin_leverage(symbol=symbol, margin_type=margin_type, leverage=leverage)


if __name__ == '__main__':
    api = CoinAPI()

    api.change_usdt_leverage('binance', 'ETHUSDT', 'CROSSED', 3)

    # try:
    #     a = api.binance.send_isolated_margin_market_order(symbol="BTCUSDT",
    #                                                       side="BUY",
    #                                                       quantity="0.04",
    #                                                       sideEffectType="MARGIN_BUY")
    # except Exception as e:
    #     print(e.code)
    #     print(dir(e))
    #     print(str(e).split("code=-")[1][:5])