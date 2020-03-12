import datetime
from unittest import TestCase

from pytz import timezone

from plugins import dateutils


class TestDateUtils(TestCase):

    def test_parse_date(self):
        now = datetime.datetime.now(timezone('Asia/Tokyo'))
        days_one = datetime.timedelta(days=1)
        expected_tomorrow = (now + days_one).date()
        expected_today = now.date()
        expected_yesterday = (now - days_one).date()
        expected_year = now.year
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
        now = datetime.datetime.now(timezone('Asia/Tokyo'))
        expected_year = now.year
        expected_hour = now.hour
        expected_minute = now.minute
        self.assertEqual(datetime.datetime(2020, 10, 20, 12, 30), dateutils.normalize_datetime('2020/10/20 12:30'))
        self.assertEqual(datetime.datetime(expected_year, 10, 20, 12, 30), dateutils.normalize_datetime('10/20 12:30'))
        self.assertEqual(datetime.datetime(2020, 10, 20, expected_hour, expected_minute),
                         dateutils.normalize_datetime('2020/10/20'))

    def test_is_am(self):
        self.assertTrue(dateutils.is_am('am休み'))
        self.assertTrue(dateutils.is_am('午前休み'))
        self.assertFalse(dateutils.is_am('pm休み'))

    def test_is_pm(self):
        self.assertTrue(dateutils.is_pm('pm休み'))
        self.assertTrue(dateutils.is_pm('午後休み'))
        self.assertFalse(dateutils.is_pm('am休み'))
