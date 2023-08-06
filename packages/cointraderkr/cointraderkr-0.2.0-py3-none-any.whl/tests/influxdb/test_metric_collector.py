from unittest import TestCase

from collectors.metric_collector import (
    MetricCollector,
    INFLUXDB_TEST_TOKEN,
    INFLUXDB_TEST_ORG,
    INFLUXDB_TEST_BUCKET,
)


class TestMetricCollector(TestCase):

    def setUp(self):
        self.mc = MetricCollector(token=INFLUXDB_TEST_TOKEN,
                                  org=INFLUXDB_TEST_ORG,
                                  bucket=INFLUXDB_TEST_BUCKET)

    def tearDown(self):
        pass

    def test_1_can_send_metrics(self):
        raise NotImplementedError

    def test_2_can_get_metrics_as_dataframe(self):
        raise NotImplementedError

    def test_3_can_get_metrics_as_list(self):
        raise NotImplementedError

    def test_4_can_set_start_from_while_get_metric(self):
        raise NotImplementedError

    def test_5_can_set_multiple_fields_while_get_metric(self):
        raise NotImplementedError

    def test_6_can_set_resample_window_while_get_metric(self):
        raise NotImplementedError