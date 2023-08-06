import os
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
application = get_wsgi_application()

from db.models import *
from api.settings import BASE_DIR

load_dotenv(override=True)

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT')


class DbHandler:

    def __init__(self,
                 user: str = DB_USER,
                 password: str = DB_PASS,
                 host: str = DB_HOST,
                 port: str = DB_PORT,
                 name: str = DB_NAME):

        if host != 'localhost':
            self.query = f'mysql://{user}:{password}@{host}:{port}/{name}?charset=utf8'
        else:
            self.query = f'sqlite:///{str(BASE_DIR / "db.sqlite3")}'

        self.conn = sqlalchemy.create_engine(self.query, pool_recycle=1)
        self.tables = self._get_tables()

        self.user = User
        self.user_profile = UserProfile
        self.log = Log
        self.pair_signal = PairSignal_Table
        self.order = Order_Table
        self.fill = Fill_Table

    def _get_tables(self) -> list:
        """
        mysql/dbsqlite3에 따라서 테이블명을 쿼리하는 방식이 다르기 때문에 seam을 생성
        --> 각 query에 따라서 SQL 쿼리 다르게 생성
        """
        if 'mysql' in self.query:
            tables = self.conn.execute(f"""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='{DB_NAME}';
            """)
        else:
            tables = self.conn.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';
            """)
        return [t[0] for t in tables]

    def _get_data(self, tablename: str) -> pd.DataFrame:
        data = pd.read_sql(f"""
        SELECT * FROM {tablename};
        """, self.conn)
        return data


if __name__ == '__main__':
    handler = DbHandler()
    print(handler.tables)