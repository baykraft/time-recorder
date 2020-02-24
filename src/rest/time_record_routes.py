from flask import Blueprint, request, jsonify
import requests
import json
import datetime
from flask_cors import CORS
from plugins.models import engine, TimeRecord
from sqlalchemy.orm import sessionmaker
from typing import List


module_api = Blueprint('times', __name__)
CORS(module_api)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['DELETE'])
def delete(year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を削除します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session: Session = Session()
        record: TimeRecord = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date == datetime.date(year, month, date)
        ).first()

        if record:
            session.delete(record)
            session.commit()
            session.close()
            return jsonify({'ok': True}), 200
        else:
            session.commit()
            session.close()
            return jsonify({'ok': False}), 404

    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['PUT'])
def update(year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を更新します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()

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
            result = __time_record_to_result(filtered)
            session.commit()
            session.close()
            return jsonify({'ok': True, 'record': result}), 200
        else:
            session.commit()
            session.close()
            return jsonify({'ok': False}), 404
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/<int:year>/<int:month>/<int:date>', methods=['POST'])
def create(year: int, month: int, date: int):
    """
    指定年月日の勤怠記録情報を登録します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param date: 日
    :type date: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()

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
            session.commit()
            session.close()
            return jsonify({'ok': False}), 409
        else:
            record: TimeRecord = TimeRecord(user, datetime.date(year, month, date))
            record.start_time = datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None
            record.end_time = datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None
            record.note = note
            record.customer = customer
            record.kind = kind
            session.add(record)
            result = __time_record_to_result(record)
            session.commit()
            session.close()
            return jsonify({'ok': True, 'record': result}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/<int:year>/<int:month>', methods=['GET'])
def records(year: int, month: int):
    """
    指定年月の勤怠記録情報を取得します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: 正常時: 勤怠記録情報リスト, 異常時: JSON形式のエラーメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()
        time_records: List[TimeRecord] = session.query(TimeRecord).filter(
            TimeRecord.user == user,
            TimeRecord.date >= datetime.date(year, month, 1),
            TimeRecord.date < datetime.date(year, month + 1, 1)
        ).all()

        results = []
        for record in time_records:
            results.append(__time_record_to_result(record))

        session.commit()
        session.close()

        return jsonify({'ok': True, 'records': results}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


def __time_record_to_result(record: TimeRecord) -> dict:
    """
    TimeRecordエンティティを辞書型オブジェクトに変換します。

    :param record: TimeRecordエンティティ
    :type record: TimeRecord
    :return: 勤怠記録情報を表す辞書型オブジェクト
    :rtype: dict
    """
    if record.start_time and record.end_time:
        dt1: datetime = datetime.datetime.combine(record.date, record.start_time)
        dt2: datetime = datetime.datetime.combine(record.date, record.end_time)
        seconds = (dt2 - dt1).total_seconds()
        m, s = divmod(seconds, 60)  # 秒を60で割った答えがm(分), 余りがs(秒)
        h, m = divmod(m, 60)        # 分を60で割った答えがh(時), 余りがm(分)
        total_time = datetime.time(hour=int(h), minute=int(m))
    else:
        total_time = None

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
        'note': record.note
    }
