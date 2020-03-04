from flask import Blueprint, request, jsonify, make_response
import requests
import json
import datetime
import logging
from flask_cors import CORS
from plugins.models import Session, TimeRecord, BreakTime, FixedTime
from typing import List
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

module_api = Blueprint('time_records', __name__)
CORS(module_api)
logger = logging.getLogger('flask.app')


@module_api.url_value_preprocessor
def url_value_preprocessor(endpoint, values):
    """
    パラメータで受け取ったトークンに対する認証を実施します。

    :param endpoint: エンドポイント
    :type endpoint: str
    :param values: パスパラメータリスト
    :type values: dict
    :return: 認証OKの場合は無し、認証NGの場合はJSONメッセージ
    :rtype: tuple[Any, int]
    """
    if 'OPTIONS' != request.method:
        token = request.args.get('token')
        r = requests.post('https://slack.com/api/auth.test', {'token': token})
        j = json.loads(r.text)
        if j['ok']:
            values['user'] = j['user_id']
        else:
            return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['DELETE'])
def delete(user: str, year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を削除します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        record: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == datetime.date(year, month, date)
        ).first()

        if record:
            session.delete(record)
            return jsonify({'ok': True}), 200
        else:
            return jsonify({'ok': False}), 404
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['PUT'])
def update(user: str, year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を更新します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        customer = request.json['customer'] if 'customer' in request.json else None
        kind = request.json['kind'] if 'kind' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None
        note = request.json['note'] if 'note' in request.json else None

        filtered: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == datetime.date(year, month, date)
        ).first()

        if filtered:
            filtered.customer = customer
            filtered.kind = kind
            filtered.start_time = datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None
            filtered.end_time = datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None
            filtered.note = note

            # 祝日を取得
            holiday_response = requests.get(f'https://holidays-jp.github.io/api/v1/{year}/date.json')
            if 200 == holiday_response.status_code:
                japanese_holidays = holiday_response.json()
            else:
                japanese_holidays = {}

            date = datetime.date(year=filtered.date.year, month=filtered.date.month, day=filtered.date.day)
            day = date.weekday()  # 0:月～6:日
            holiday_key = '{0:%Y-%m-%d}'.format(date)
            holiday = (day == 5 or day == 6 or holiday_key in japanese_holidays)
            holiday_note = japanese_holidays[holiday_key] if holiday_key in japanese_holidays else None
            result = __time_record_to_result(session, user, date, holiday, holiday_note, filtered)

            return jsonify({'ok': True, 'record': result}), 200
        else:
            return jsonify({'ok': False}), 404
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['POST'])
def create(user: str, year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を登録します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        customer = request.json['customer'] if 'customer' in request.json else None
        kind = request.json['kind'] if 'kind' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None
        note = request.json['note'] if 'note' in request.json else None

        filtered: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == datetime.date(year, month, date)
        ).first()

        if filtered:
            return jsonify({'ok': False}), 409
        else:
            record: TimeRecord = TimeRecord(user, datetime.date(year, month, date))
            record.start_time = datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None
            record.end_time = datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None
            record.note = note
            record.customer = customer
            record.kind = kind
            session.add(record)
            session.flush()

            # 祝日を取得
            holiday_response = requests.get(f'https://holidays-jp.github.io/api/v1/{year}/date.json')
            if 200 == holiday_response.status_code:
                japanese_holidays = holiday_response.json()
            else:
                japanese_holidays = {}

            date = datetime.date(year=record.date.year, month=record.date.month, day=record.date.day)
            day = date.weekday()  # 0:月～6:日
            holiday_key = '{0:%Y-%m-%d}'.format(date)
            holiday = (day == 5 or day == 6 or holiday_key in japanese_holidays)
            holiday_note = japanese_holidays[holiday_key] if holiday_key in japanese_holidays else None
            result = __time_record_to_result(session, user, date, holiday, holiday_note, record)

            return jsonify({'ok': True, 'record': result}), 201
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:year>/<int:month>', methods=['GET'])
def records(user: str, year: int, month: int):
    """
    指定年月の勤怠記録情報を取得します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: 正常時: 勤怠記録情報リスト, 異常時: JSON形式のエラーメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        time_records: List[TimeRecord] = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date >= datetime.date(year, month, 1),
            TimeRecord.date < datetime.date(year, month + 1, 1)
        ).all()

        # 祝日を取得
        holiday_response = requests.get(f'https://holidays-jp.github.io/api/v1/{year}/date.json')
        if 200 == holiday_response.status_code:
            japanese_holidays = holiday_response.json()
        else:
            japanese_holidays = {}

        results = []
        date = datetime.date(year, month, 1)
        while month == date.month:
            day = date.weekday()  # 0:月～6:日
            holiday_key = '{0:%Y-%m-%d}'.format(date)
            holiday = (day == 5 or day == 6 or holiday_key in japanese_holidays)
            target_record = next(
                filter(lambda r: r.date.year == year and r.date.month == month and r.date.day == date.day,
                       time_records), None)
            holiday_note = japanese_holidays[holiday_key] if holiday_key in japanese_holidays else None
            results.append(__time_record_to_result(session, user, date, holiday, holiday_note, target_record))
            date = date + datetime.timedelta(days=1)

        return jsonify({'ok': True, 'records': results}), 200
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:year>/<int:month>/download', methods=['GET'])
def download(user: str, year: int, month: int):
    """
    勤怠記録をExcelファイルでダウンロードします。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: Excelファイル
    :rtype: Any
    """
    session = Session()
    try:
        time_records: List[TimeRecord] = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date >= datetime.date(year, month, 1),
            TimeRecord.date < datetime.date(year, month + 1, 1)
        ).all()

        # 祝日を取得
        holiday_response = requests.get(f'https://holidays-jp.github.io/api/v1/{year}/date.json')
        if 200 == holiday_response.status_code:
            japanese_holidays = holiday_response.json()
        else:
            japanese_holidays = {}

        # 日付毎の勤怠記録を生成
        results = []
        date = datetime.date(year, month, 1)
        while month == date.month:
            day = date.weekday()  # 0:月～6:日
            holiday_key = '{0:%Y-%m-%d}'.format(date)
            holiday = (day == 5 or day == 6 or holiday_key in japanese_holidays)
            target_record = next(
                filter(lambda r: r.date.year == year and r.date.month == month and r.date.day == date.day,
                       time_records), None)
            holiday_note = japanese_holidays[holiday_key] if holiday_key in japanese_holidays else None
            results.append(__time_record_to_result(session, user, date, holiday, holiday_note, target_record))
            date = date + datetime.timedelta(days=1)

        # Excelとして出力
        wb = load_workbook('resources/template.xlsx')
        ws = wb['勤怠']
        row_index = 2
        day_of_week = '月', '火', '水', '木', '金', '土', '日'
        kind = {
            '0': '',
            '10': '有休', '11': '有休(AM)', '12': '有休(PM)',
            '20': '欠勤', '21': '欠勤(AM)', '22': '欠勤(PM)',
            '30': '特休', '31': '特休(AM)', '32': '特休(PM)',
            '40': '代休', '41': '代休(AM)', '42': '代休(PM)',
            '50': '休出'
        }
        for result in results:
            ws.cell(row=row_index, column=1).value = result['date']
            ws.cell(row=row_index, column=2).value = day_of_week[result['day']]
            ws.cell(row=row_index, column=3).value = 'H' if result['holiday'] else None
            ws.cell(row=row_index, column=4).value = result['customer']
            ws.cell(row=row_index, column=5).value = kind[str(result['kind'])]
            ws.cell(row=row_index, column=6).value = __to_time(result['start_time'])
            ws.cell(row=row_index, column=7).value = __to_time(result['end_time'])
            ws.cell(row=row_index, column=8).value = __to_time(result['total_time'])
            ws.cell(row=row_index, column=9).value = result['note']
            row_index += 1

        res = make_response(save_virtual_workbook(wb))
        res.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        res.headers['Content-Disposition'] = 'attachment; filename=sample.xlsx'
        return res
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


def __to_time(time: str) -> datetime.time:
    """
    時間文字列をdatetime.timeオブジェクトに変換します。

    :param time: 時間文字列
    :type time: str
    :return: datetime.timeオブジェクト
    :rtype: datetime.time
    """
    if time:
        return datetime.datetime.strptime(time, '%H:%M').time()


def __calc_total_time(break_times: List[BreakTime], record: TimeRecord) -> datetime.time:
    """
    合計時間を算出します。

    :param break_times: 休憩時間リスト
    :type break_times: List[BreakTime]
    :param record: TimeRecordエンティティ
    :type record: TimeRecord
    :return: 合計時間
    :rtype: datetime.time
    """
    dt1: datetime = datetime.datetime.combine(record.date, record.start_time)
    dt2: datetime = datetime.datetime.combine(record.date, record.end_time)
    seconds: float = (dt2 - dt1).total_seconds()

    # 稼働時間から休憩時間を控除
    for break_time in break_times:
        bt1: datetime = datetime.datetime.combine(record.date, break_time.start_time)
        bt2: datetime = datetime.datetime.combine(record.date, break_time.end_time)
        if bt2 > dt1 and bt1 < dt2:
            start: datetime = dt1 if dt1 > bt1 else bt1
            end: datetime = dt2 if dt2 < bt2 else bt2
            seconds = seconds - (end - start).total_seconds()

    # 休憩時間を控除した稼働時間をdatetime.time型に変換
    m, s = divmod(seconds, 60)  # 秒を60で割った答えがm(分), 余りがs(秒)
    h, m = divmod(m, 60)  # 分を60で割った答えがh(時), 余りがm(分)
    return datetime.time(hour=int(h), minute=int(m))


def __calc_over_time(fixed_times: List[FixedTime], record: TimeRecord) -> datetime.time:
    """
    残業時間を算出します。

    :param fixed_times: 所定時間リスト
    :type fixed_times: List[FixedTime]
    :param record: TimeRecordエンティティ
    :type record: TimeRecord
    :return: 残業時間
    :rtype: datetime.time
    """
    dt2: datetime = datetime.datetime.combine(record.date, record.end_time)
    seconds: float = 0

    # 所定時間を超える部分の時間を算出
    for fixed_time in fixed_times:
        ft2: datetime = datetime.datetime.combine(record.date, fixed_time.end_time)
        if ft2 < dt2:
            seconds: float = (dt2 - ft2).total_seconds()
        break

    m, s = divmod(seconds, 60)  # 秒を60で割った答えがm(分), 余りがs(秒)
    h, m = divmod(m, 60)  # 分を60で割った答えがh(時), 余りがm(分)
    return datetime.time(hour=int(h), minute=int(m))


def __time_record_to_result(
        session, user: str, date: datetime.date, holiday: bool, holiday_note: str, record: TimeRecord) -> dict:
    """
    TimeRecordエンティティを辞書型オブジェクトに変換します。

    :param session: DBセッション
    :type session: Any
    :param user: ユーザID
    :type user: str
    :param date: 日付
    :type date: datetime.date
    :param holiday: 祝日フラグ
    :type holiday: bool
    :param holiday_note: 祝日ノート
    :type holiday_note: str
    :param record: TimeRecordエンティティ
    :type record: TimeRecord
    :return: 勤怠記録情報を表す辞書型オブジェクト
    :rtype: dict
    """
    if record and record.start_time and record.end_time:

        # 指定された客先の休憩時間リストを取得
        break_times: List[BreakTime] = session.query(BreakTime).filter(
            BreakTime.user == user,
            BreakTime.year == record.date.year,
            BreakTime.month == record.date.month,
            BreakTime.customer == record.customer
        ).all()

        # 指定された客先の所定時間リストを取得
        fixed_times: List[FixedTime] = session.query(FixedTime).filter(
            FixedTime.user == user,
            FixedTime.year == record.date.year,
            FixedTime.month == record.date.month,
            FixedTime.customer == record.customer
        ).all()

        total_time = __calc_total_time(break_times, record)
        over_time = __calc_over_time(fixed_times, record)
    else:
        total_time = None
        over_time = None

    return {
        'time_record_id': record.time_record_id if record else 0,
        'year': record.date.year if record else date.year,
        'month': record.date.month if record else date.month,
        'date': record.date.day if record else date.day,
        'day': date.weekday(),
        'holiday': holiday,
        'customer': record.customer if record else None,
        'kind': record.kind if record else 0,
        'start_time': '{0:%H:%M}'.format(record.start_time) if record and record.start_time else None,
        'end_time': '{0:%H:%M}'.format(record.end_time) if record and record.end_time else None,
        'total_time': '{0:%H:%M}'.format(total_time) if total_time else None,
        'over_time': '{0:%H:%M}'.format(over_time) if over_time else None,
        'note': record.note if record else holiday_note
    }
