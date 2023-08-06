import os
import paramiko
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)


class FileServer:
    """
    Server로의 연결을 담당하고 있는 클래스

    server_type: 1, 2, ...

    1을 인자로 넣을 경우 서버 1에 연결을 시도한다.
    2를 인자로 넣을 경우 서버 2에 연결을 시도한다.
    """

    from_path = Path(os.path.expanduser("~")) / "coin-trader-cache"
    to_path = Path(os.path.expanduser("~")) / "ftp-cache"

    SERVER_1_HOST = os.getenv('SERVER_1_HOST')
    SERVER_1_USER = os.getenv('SERVER_1_USER')
    SERVER_1_PASS = os.getenv('SERVER_1_PASS')
    SERVER_1_PORT = os.getenv('SERVER_1_PORT')

    SERVER_2_HOST = os.getenv('SERVER_2_HOST')
    SERVER_2_USER = os.getenv('SERVER_2_USER')
    SERVER_2_PASS = os.getenv('SERVER_2_PASS')
    SERVER_2_PORT = os.getenv('SERVER_2_PORT')

    def __init__(self, server_type: int):
        self.host = getattr(self, f'SERVER_{server_type}_HOST')
        self.user = getattr(self, f'SERVER_{server_type}_USER')
        self.password = getattr(self, f'SERVER_{server_type}_PASS')

        self._connect()

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host,
                         username=self.user,
                         password=self.password)
        self.sftp = self.ssh.open_sftp()
        self.sftp.chdir('FTP') # 모든 FTP 관련 파일은 서버의 /root/FTP 폴더에 있어야 한다.

    def ls(self, dirname: str = None):
        if dirname is None:
            return self.sftp.listdir()
        else:
            return self.sftp.listdir(dirname)

    def mkdir(self, dirname: str):
        try:
            self.sftp.mkdir(dirname)
        except OSError:
            # directory 이미 존재함
            return None

    def rmdir(self, dirname: str):
        """
        USE WITH CAUTION!
        """
        self.sftp.rmdir(dirname)

    def exists(self, dirname: str):
        try:
            self.sftp.stat(dirname)
            return True
        except FileNotFoundError:
            return False

    def upload(self, source: str, name: str, file_type: str = 'h5'):
        """

        :param source: kiwoom, ebest, shinhan, binance, bybit, upbit, etc.
        :param market: futures, stock, spot, coinm, etc.
        :param name: 20210101, BTCUSDT, etc.
        :param file_type: h5, zst, csv, etc.
        :return:
        """
        if not self.exists(f'./{source}'):
            self.mkdir(f'./{source}')

        from_file = str(self.from_path / source / f'{name}.{file_type}')
        to_file = f'./{source}/{name}.{file_type}'

        self.sftp.put(from_file, to_file)

    def download(self, source: str, name: str, file_type: str = 'h5'):
        if not os.path.exists(self.to_path / source):
            os.makedirs(self.to_path / source)

        from_file = f'./{source}/{name}.{file_type}'
        to_file = str(self.from_path / source / f'{name}.{file_type}')

        self.sftp.put(from_file, to_file)


if __name__ == '__main__':
    fs = FileServer(server_type=1)
    print(fs)