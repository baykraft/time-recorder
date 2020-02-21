import datetime
from pytz import timezone
from plugins import stringutils
import re


def parse_date(value: str) -> datetime.date:
    """
    文字列から日付を取得します。

    :param value: 文字列
    :type value: str
    :return: 日付
    :rtype: datetime.date
    """
    # 全角英数字記号を半角英数字記号に変換
    value = stringutils.translate2han(value)
    days_one = datetime.timedelta(days=1)
    now = datetime.datetime.now(timezone('Asia/Tokyo'))
    if re.search('(明日|tomorrow)', value):
        return (now + days_one).date()
    if re.search('(今日|today)', value):
        return now.date()
    if re.search('(昨日|yesterday)', value):
        return (now - days_one).date()

    # 日付が直接指定された場合はその日付を返却
    pattern = re.compile(r'((\d{4})[-/年]|)(\d{1,2})[-/月](\d{1,2})')
    matches = pattern.search(value)
    if matches:
        groups = matches.group(2, 3, 4)
        year = int(now.year if (groups[0] is None) else groups[0])
        month = int(groups[1])
        day = int(groups[2])
        return datetime.date(year=year, month=month, day=day)


def parse_time(value: str):
    """
    文字列から時間を取得します。

    :param value: 文字列
    :type value: str
    :return: 時間
    :rtype: datetime.time
    """
    # 全角英数字記号を半角英数字記号に変換
    value = stringutils.translate2han(value)
    pattern = re.compile(r'((\d{1,2})\s*[:時]\s*(\d{1,2})\s*(pm|)|'
                         r'(am|pm|午前|午後)\s*(\d{1,2})(\s*[:時]\s*(\d{1,2})|)|'
                         r'(\d{1,2})(\s*[:時]\s*(\d{1,2})|)(am|pm)|'
                         r'(\d{1,2})\s*時)')
    matches = pattern.search(value)
    if matches:
        groups = matches.groups()
        hour = 0
        minute = 0
        # 13時20, 14:30, 3:00pm
        if groups[1] is not None:
            hour = int(groups[1])
            minute = int(groups[2])
            if 'pm' in groups[3]:
                hour += 12
        # 午後1, 午後2時30, pm3
        if groups[4] is not None:
            hour = int(groups[5])
            minute = int(groups[7] or 0)
            if 'pm' in groups[4] or '午後' in groups[4]:
                hour += 12
        # 1pm
        if groups[8] is not None:
            hour = int(groups[8])
            minute = int(groups[10] or 0)
            if 'pm' in groups[11]:
                hour += 12
        # 14時
        if groups[12] is not None:
            hour = int(groups[12])

        hour = 0 if hour > 23 else hour
        minute = 0 if minute > 59 else minute
        return datetime.time(hour=hour, minute=minute)


def normalize_datetime(message: str) -> datetime.datetime:
    """
    文字列から日時を取得します。

    :param message: 文字列
    :type message: str
    :return: 日時
    :rtype: datetime.datetime
    """
    now = datetime.datetime.now(timezone('Asia/Tokyo'))
    date = parse_date(message) or now.date()
    time = parse_time(message) or now.time()
    time = time.replace(second=0, microsecond=0)
    return datetime.datetime.combine(date, time)
