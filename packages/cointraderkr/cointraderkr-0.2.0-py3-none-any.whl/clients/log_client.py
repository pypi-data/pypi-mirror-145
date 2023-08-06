import json
import logging
import requests


class TraderLogHandler(logging.StreamHandler):

    def __init__(self, logger_name: str = 'trader_logger', ip_address: str = '127.0.0.1'):
        super().__init__()

        self.logger_name = logger_name
        self.ip_address = ip_address

        fmt = {
            'source': self.logger_name,
            'ip_address': self.ip_address,
            'log_level': '%(levelname)s',
            'timestamp': '%(asctime)s',
            'filename': '%(filename)s:%(lineno)d',
            'message': '%(message)s'
        }
        formatter = logging.Formatter(json.dumps(fmt))
        self.setFormatter(formatter)

    def emit(self, record):
        data = json.loads(self.format(record))
        res = requests.post('http://api.blended.kr/log', data=json.dumps(data))
        if res.json()['status'] == 'FAILED':
            raise Exception(res.json())


class TraderLogger:

    def __init__(self,
                 logger_name: str = 'trader_logger',
                 ip_address: str = '127.0.0.1',
                 print_log: bool = True):

        self.print_log = print_log

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        handler = TraderLogHandler(logger_name, ip_address)
        self.logger.addHandler(handler)

    def debug(self, log: str):
        if self.print_log:
            print(log)
        log = log.replace('\n', '\\n')
        self.logger.debug(log)

    def info(self, log: str):
        if self.print_log:
            print(log)
        log = log.replace('\n', '\\n')
        self.logger.info(log)

    def error(self, log: str):
        if self.print_log:
            print(log)
        log = log.replace('\n', '\\n')
        self.logger.error(log)

    def exception(self, log: str):
        if self.print_log:
            print(log)
        log = log.replace('\n', '\\n')
        self.logger.exception(log)


if __name__ == '__main__':
    logger = TraderLogger()
    logger.info('hello there 2')