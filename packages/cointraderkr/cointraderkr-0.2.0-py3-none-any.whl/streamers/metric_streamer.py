from multiprocessing import Queue
from tradernetwork import PullSocket, PubSocket


class MetricStreamer:
    """
    MetricStreamer는 FastAPI를 끼고 하지 않고, 따로 도커 컨테이너로 올린다.
    이렇게 하면 여러개 프로세스를 열어서 metric data를 병렬로 저장할 수 있게 된다.
    """

    def __init__(self,
                 pub_port: int = 1215,
                 pull_port: int = 1216,
                 q1: Queue = None,
                 q2: Queue = None,
                 q3: Queue = None):

        self.pub_socket = PubSocket(pub_port)
        self.pull_socket = PullSocket(pull_port)

        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

        self.queues = [self.q1, self.q2, self.q3]

    def start(self):
        print('[MetricStreamer] Starting Pub / Pull servers')

        i = 0

        while True:
            data = self.pull_socket._recv()
            self.queues[i].put(data)

            points = data['points']

            for pt in points:
                self.pub_socket.publish(pt)

            i += 1

            if i == 3:
                i = 0