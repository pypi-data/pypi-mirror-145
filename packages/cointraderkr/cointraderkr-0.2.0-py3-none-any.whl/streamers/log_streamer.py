from tradernetwork import PullSocket, PubSocket


class LogStreamer:

    def __init__(self, pub_port: int = 1213, pull_port: int = 1214):
        self.pub_socket = PubSocket(pub_port)
        self.pull_socket = PullSocket(pull_port)

    def start(self):
        print('[LogStreamer] Starting Pub / Pull servers')
        while True:
            data = self.pull_socket._recv()
            self.callback(data)

    def callback(self, data: dict):
        self.pub_socket.publish(data)


if __name__ == '__main__':
    streamer = LogStreamer(1002, 1003)
    streamer.start()