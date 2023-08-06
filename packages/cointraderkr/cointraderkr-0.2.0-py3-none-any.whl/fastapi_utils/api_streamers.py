from streamers.log_streamer import LogStreamer
from streamers.data_streamer import DataStreamer


def start_log_streamer(pub_port: int, pull_port: int):
    streamer = LogStreamer(pub_port, pull_port)
    streamer.start()


def start_data_streamer(pub_port: int, rep_port: int):
    streamer = DataStreamer(pub_port, rep_port)
    streamer.start()


if __name__ == '__main__':
    import time
    import threading

    t = threading.Thread(target=start_data_streamer, args=(900, 901))
    t.start()

    while True:
        time.sleep(5)