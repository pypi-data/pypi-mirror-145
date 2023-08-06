import os
import threading
from dotenv import load_dotenv
from collections import deque
from tradernetwork import (
    SubSocket,
    PubSocket,
    RepSocket,
    ProxySocket,
)

load_dotenv(override=True)

SERVER_1_HOST = os.getenv('SERVER_1_HOST')
SERVER_2_HOST = os.getenv('SERVER_2_HOST')


class DataStreamer:

    sec_price_data = {}

    def __init__(self, pub_port: int = 1211, rep_port: int = 1212):
        sockets = {
            'data': SubSocket(4011, SERVER_1_HOST)
        }

        self.proxy = ProxySocket(sockets)
        self.proxy.callback = self.callback

        self.pub_socket = PubSocket(pub_port)
        self.rep_server = RepServer(rep_port, self)

    def start(self):
        print('[DataStreamer] Starting Proxy / Rep servers')

        t1 = threading.Thread(target=self.proxy.start_proxy_server_loop)
        t1.start()

        t2 = threading.Thread(target=self.rep_server.start_rep_server_loop)
        t2.start()

    def callback(self, socket_name: str, data: dict):
        if data['source'] in ['bybit_sec_svc', 'binance_sec_svc']:
            source = data['source']

            if source in ['bybit_sec_svc', 'binance_sec_svc']:
                exchange = data['data']['source']
                asset_type = data['data']['symbol'].split('.')[0]
                symbol = data['data']['symbol'].split('.')[-1]

                key = f'{exchange}.{asset_type}.{symbol}'

                if key not in self.sec_price_data:
                    self.sec_price_data[key] = deque([], maxlen=600)

                self.sec_price_data[key].append(data['data']['data']['current_price'])

                data = {'server': data['server'], **data['data']}
                self.pub_socket.publish(data)


class RepServer(RepSocket):

    def __init__(self, port: int, streamer: DataStreamer):
        super().__init__(port)

        self.streamer = streamer

    def get_sec_price_data(self, symbol: str = None, **kwargs):
        """
        symbol: bybit.usdt.BTCUSDT
        """
        sec_price_data = {key: list(val) for key, val in self.streamer.sec_price_data.items()}
        if symbol is not None:
            try:
                sec_price_data = sec_price_data[symbol]
                return True, '', sec_price_data
            except Exception as e:
                error_msg = str(e)
                return False, error_msg, None
        else:
            return True, '', sec_price_data


if __name__ == '__main__':
    streamer = DataStreamer(1000, 1001)
    streamer.start()

    import time

    while True:
        time.sleep(5)