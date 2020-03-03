from flask import Blueprint, request, jsonify
import requests
import json
import datetime
import logging
from flask_cors import CORS
from plugins.models import engine, TimeRecord, BreakTime, FixedTime
from sqlalchemy.orm import sessionmaker
from typing import List


module_api = Blueprint('time_records', __name__)
CORS(module_api)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)
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
    session: Session = Session()
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
        logger.error(e)
    finally:
        if session.is_active():
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
    session: Session = Session()
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
            result = __time_record_to_result(user, filtered)
            return jsonify({'ok': True, 'record': result}), 200
        else:
            return jsonify({'ok': False}), 404
    except Exception as e:
        session.rollback()
        logger.error(e)
    finally:
        if session.is_active():
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
    session: Session = Session()
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
            result = __time_record_to_result(user, record)
            return jsonify({'ok': True, 'record': result}), 200
    except Exception as e:
        session.rollback()
        logger.error(e)
    finally:
        if session.is_active():
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
    session: Session = Session()
    try:
        time_records: List[TimeRecord] = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date >= datetime.date(year, month, 1),
            TimeRecord.date < datetime.date(year, month + 1, 1)
        ).all()

        results = []
        for record in time_records:
            results.append(__time_record_to_result(user, record))

        return jsonify({'ok': True, 'records': results}), 200
    except Exception as e:
        session.rollback()
        logger.error(e)
    finally:
        if session.is_active():
            session.commit()
        session.close()


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


def __time_record_to_result(user: str, record: TimeRecord) -> dict:
    """
    TimeRecordエンティティを辞書型オブジェクトに変換します。

    :param user: ユーザID
    :param user: str
    :param record: TimeRecordエンティティ
    :type record: TimeRecord
    :return: 勤怠記録情報を表す辞書型オブジェクト
    :rtype: dict
    """
    session: Session = Session()
    try:
        if record.start_time and record.end_time:

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
            'time_record_id': record.time_record_id,
            'year': record.date.year,
            'month': record.date.month,
            'date': record.date.day,
            'customer': record.customer,
            'kind': record.kind,
            'start_time': '{0:%H:%M}'.format(record.start_time) if record.start_time else None,
            'end_time': '{0:%H:%M}'.format(record.end_time) if record.end_time else None,
            'total_time': '{0:%H:%M}'.format(total_time) if total_time else None,
            'over_time': '{0:%H:%M}'.format(over_time) if over_time else None,
            'note': record.note
        }
    except Exception as e:
        session.rollback()
        logger.error(e)
    finally:
        if session.is_active():
            session.commit()
        session.close()
