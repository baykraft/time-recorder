from unittest import TestCase
from plugins import dateutils
import datetime


class TestDateUtils(TestCase):

    def test_parse_date(self):
        expected_tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
        expected_today = datetime.datetime.today().date()
        expected_yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
        expected_year = datetime.datetime.today().year
        self.assertEqual(expected_tomorrow, dateutils.parse_date('明日'))
        self.assertEqual(expected_today, dateutils.parse_date('今日'))
        self.assertEqual(expected_yesterday, dateutils.parse_date('昨日'))
        self.assertEqual(expected_tomorrow, dateutils.parse_date('tomorrow'))
        self.assertEqual(expected_today, dateutils.parse_date('today'))
        self.assertEqual(expected_yesterday, dateutils.parse_date('yesterday'))
        self.assertEqual(datetime.date(2020, 10, 20), dateutils.parse_date('2020/10/20'))
        self.assertEqual(datetime.date(expected_year, 10, 20), dateutils.parse_date('10/20'))

    def test_parse_time(self):
        self.assertEqual(datetime.time(0, 0), dateutils.parse_time('12:00pm'))
        self.assertEqual(datetime.time(15, 0), dateutils.parse_time('3:00pm'))
        self.assertEqual(datetime.time(15, 0), dateutils.parse_time('3:00 pm'))
        self.assertEqual(datetime.time(12, 0), dateutils.parse_time('12:00'))
        self.assertEqual(datetime.time(12, 40), dateutils.parse_time('12時40'))
        self.assertEqual(datetime.time(0, 0), dateutils.parse_time('午後12:00'))
        self.assertEqual(datetime.time(13, 0), dateutils.parse_time('午後1'))
        self.assertEqual(datetime.time(15, 20), dateutils.parse_time('pm3:20'))
        self.assertEqual(datetime.time(13, 0), dateutils.parse_time('1pm'))
        self.assertEqual(datetime.time(14, 0), dateutils.parse_time('14時'))
        self.assertEqual(datetime.time(12, 0), dateutils.parse_time('12:60'))

    def test_normalize_datetime(self):
        expected_year = datetime.datetime.today().year
        expected_hour = datetime.datetime.now().hour
        expected_minute = datetime.datetime.now().minute
        self.assertEqual(datetime.datetime(2020, 10, 20, 12, 30), dateutils.normalize_datetime('2020/10/20 12:30'))
        self.assertEqual(datetime.datetime(expected_year, 10, 20, 12, 30), dateutils.normalize_datetime('10/20 12:30'))
        self.assertEqual(datetime.datetime(2020, 10, 20, expected_hour, expected_minute),
                         dateutils.normalize_datetime('2020/10/20'))
