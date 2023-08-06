import os
import pytz
import pandas as pd
from dotenv import load_dotenv
from typing import Any, List, Dict
from datetime import datetime, timezone

from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision

load_dotenv(override=True)

INFLUXDB_HOST = os.getenv('INFLUXDB_HOST')

INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

INFLUXDB_TEST_TOKEN = os.getenv('INFLUXDB_TEST_TOKEN')
INFLUXDB_TEST_ORG = os.getenv('INFLUXDB_TEST_ORG')
INFLUXDB_TEST_BUCKET = os.getenv('INFLUXDB_TEST_BUCKET')


class MetricCollector:

    def __init__(self,
                 host: str = INFLUXDB_HOST,
                 token: str = INFLUXDB_TOKEN,
                 org: str = INFLUXDB_ORG,
                 bucket: str = INFLUXDB_BUCKET,
                 sync: bool = True):

        self.host = host
        self.token = token
        self.org = org
        self.bucket = bucket

        self.kr_tz = pytz.timezone('Asia/Seoul')
        self.client = InfluxDBClient(url=self.host, token=self.token)

        self.bucket_api = self.client.buckets_api()
        if sync:
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        else:
            self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)
        self.query_api = self.client.query_api()

    def use_bucket(self, bucket: str):
        self.bucket = bucket

    def create_bucket(self, bucket_name: str):
        self.bucket_api.create_bucket(bucket_name=bucket_name, org_id=self.org)
        self.use_bucket(bucket_name)

    def delete_bucket(self, bucket_name: str):
        bucket_id = self.bucket_api.find_bucket_by_name(bucket_name)
        self.bucket_api.delete_bucket(bucket_id)

    def _point(self, measurement: str, field: str, value: float, **kwargs):
        point = Point(measurement)
        for tag_name, tag_value in kwargs.items():
            if tag_name != 'time':
                point = point.tag(tag_name, tag_value)
        if 'time' not in kwargs:
            point = point.field(field, value).time(datetime.utcnow(), WritePrecision.NS)
        else:
            timestamp = datetime.strptime(kwargs['time'], '%Y%m%d%H%M%S')
            utc_timestamp = datetime.fromtimestamp(timestamp.timestamp(), timezone.utc)
            point = point.field(field, value).time(utc_timestamp, WritePrecision.NS)
        return point

    def send_metric(self, measurement: str, field: str, value: Any, **kwargs):
        point = self._point(measurement, field, float(value), **kwargs)
        self.write_api.write(self.bucket, self.org, point)

    def send_metrics(self, data: List[Dict[str, Any]]):
        points = []
        for d in data:
            if 'value' in d:
                d['value'] = float(d['value'])
            point = self._point(**d)
            points.append(point)
        self.write_api.write(self.bucket, self.org, points)

    def _pivot(self, data: pd.DataFrame):
        return data.pivot_table(index='_time',
                                columns='_field',
                                values='_value').ffill()

    def get_metric(self,
                   bucket: str,
                   start_from: str,
                   measurement: str = None,
                   fields: List[str] = [],
                   filters: Dict[str, Any] = {},
                   window: str = '1s',
                   aggfunc: str = 'last',
                   pivot: bool = False,
                   for_api: bool = False):
        """
        :param start: -5m, -10m
        :param measurement: test_data
        :param field: diff
        :param window: 1s, 5s, 10s
        :param aggfunc: last, mean, median
        :param fmt: df, list
        :return:
        """
        fields = ' or '.join([
            f'(r["_field"] == "{field}")' for field in fields
        ])
        all_filters = ''
        for filter_key, filter_val in filters.items():
            filter_str = f'|> filter(fn: (r) => r["{filter_key}"] == "{filter_val}")'
            all_filters = f'{all_filters}{filter_str}'

        query = f"""
        from(bucket: "{bucket}")
          |> range(start: {start_from})
          {f'|> filter(fn: (r) => r["_measurement"] == "{measurement}")' if measurement is not None else ''}
          {f'|> filter(fn: (r) => {fields})' if fields else ''}
          {all_filters}
          |> aggregateWindow(every: {window}, fn: {aggfunc}, createEmpty: false)
        """

        result = self.query_api.query_data_frame(org=self.org, query=query)
        result['_time'] = pd.DatetimeIndex(result['_time']).tz_convert(self.kr_tz)

        if pivot:
            pivot_table = self._pivot(result)
            if not for_api:
                return pivot_table
            else:
                pivot_table.reset_index(inplace=True)
                pivot_table['_time'] = pivot_table['_time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M:%S'))
                return pivot_table
        else:
            if not for_api:
                result['_start'] = pd.DatetimeIndex(result['_start']).tz_convert(self.kr_tz)
                result['_stop'] = pd.DatetimeIndex(result['_stop']).tz_convert(self.kr_tz)
            else:
                result.drop(['_start', '_stop'], axis=1, inplace=True)
                result['_time'] = result['_time'].apply(lambda t: t.strftime('%Y-%m-%d %H:%M:%S'))
            return result


if __name__ == '__main__':
    import time
    import random

    mc = MetricCollector()
    mc.use_bucket('coin-trader')

    for d in range(0, 100):
        num = random.random()
        points = [
            {'measurement': 'random_data', 'field': 'volatility', 'value': num, 'strategy': 'st_1', 'chart': 'chart1'},
            {'measurement': 'random_data', 'field': 'ma_20', 'value': num + 1, 'strategy': 'st_1', 'chart': 'chart2'},
            {'measurement': 'random_data', 'field': 'garch_1', 'value': num * 2, 'strategy': 'st_1', 'chart': 'chart1'},
            {'measurement': 'random_data', 'field': 'spread', 'value': num - 10, 'strategy': 'st_1', 'chart': 'chart1'},
        ]
        mc.send_metrics(points)

        time.sleep(2)
        print(d)

    # metrics = mc.get_metric(bucket='coin-trader',
    #                         start_from='-3d',
    #                         measurement='test_data',
    #                         # fields=['volatility', 'ma_20'],
    #                         filters={'chart': 'chart1', 'strategy': 'st_1'},
    #                         window='10m',
    #                         aggfunc='mean',
    #                         pivot=True,
    #                         for_api=True)
    # print(metrics)