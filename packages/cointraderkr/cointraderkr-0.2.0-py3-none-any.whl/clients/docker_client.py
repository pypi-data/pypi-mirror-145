import json
import requests


class DockerClient:

    TOKEN_URL = 'https://api.blended.kr/access-token'
    REQUEST_URL = 'https://api.blended.kr/docker'
    STATUS_URL = 'https://api.blended.kr/task'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        params = {
            'username': self.username,
            'password': self.password
        }
        res = requests.post(self.TOKEN_URL, data=json.dumps(params))
        return res.json()['access_token']

    def restart(self, server: int, container: str):
        params = {
            'action': 'restart',
            'access_token': self.access_token,
            'server': server,
            'container': container
        }
        res = requests.post(self.REQUEST_URL, data=json.dumps(params))
        return res.json()['message']

    def status(self, task_id: str):
        params = {
            'access_token': self.access_token,
            'task_id': task_id
        }
        res = requests.post(self.STATUS_URL, data=json.dumps(params))
        return res.json()['message']


if __name__ == '__main__':
    import time

    client = DockerClient('coin.trader.korea@gmail.com', 'makeitpopweCOIN!1')

    task_id = client.restart(2, 'bybit_market_svc')

    done = False

    while not done:
        time.sleep(2)
        status = client.status(task_id)
        print(status)
        if status == 'SUCCESS':
            done = True