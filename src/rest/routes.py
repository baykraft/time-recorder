from flask import Blueprint, request, jsonify
import requests
import json
import datetime
from flask_cors import CORS
from plugins.models import engine, Timesheet
from sqlalchemy.orm import sessionmaker
from typing import List

module_api = Blueprint('rest', __name__)
CORS(module_api)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@module_api.route('/hello')
def hello():
    return 'Hello, World!'


@module_api.route('/times/<int:year>/<int:month>/<int:date>', methods=['DELETE'])
def delete(year: int, month: int, date: int):
    """
    指定年月日の勤怠情報を削除します。

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
        record: Timesheet = session.query(Timesheet).filter(
            Timesheet.user == user,
            Timesheet.date == datetime.date(year, month, date)
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


@module_api.route('/times/<int:year>/<int:month>/<int:date>', methods=['PUT'])
def create(year: int, month: int, date: int):
    """
    指定年月日の勤怠情報を更新します。

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
        record: Timesheet = session.query(Timesheet).filter(
            Timesheet.user == user,
            Timesheet.date == datetime.date(year, month, date)
        ).first()

        customer = request.json['customer'] if 'customer' in request.json else None
        kind = request.json['kind'] if 'kind' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None
        note = request.json['note'] if 'note' in request.json else None

        if record:
            record.customer = customer
            record.kind = kind
            if start_time:
                record.start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
            if end_time:
                record.end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
            record.note = note
            result = __timesheet_to_result(record)
        else:
            timesheet: Timesheet = Timesheet(user, datetime.date(year, month, date))
            if start_time:
                timesheet.start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
            if end_time:
                timesheet.end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
            timesheet.note = note
            timesheet.customer = customer
            timesheet.kind = kind
            session.add(timesheet)
            result = __timesheet_to_result(timesheet)

        session.commit()
        session.close()

        return jsonify({'ok': True, 'record': result}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/times/<int:year>/<int:month>')
def times(year: int, month: int):
    """
    指定年月の勤怠情報を取得します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: 正常時: 勤怠情報リスト, 異常時: JSON形式のエラーメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()
        records: List[Timesheet] = session.query(Timesheet).filter(
            Timesheet.user == user,
            Timesheet.date >= datetime.date(year, month, 1),
            Timesheet.date < datetime.date(year, month + 1, 1)
        ).all()

        results = []
        for record in records:
            results.append(__timesheet_to_result(record))

        session.commit()
        session.close()

        return jsonify({'ok': True, 'records': results}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


def __timesheet_to_result(record: Timesheet) -> dict:
    """
    Timesheetエンティティを辞書型オブジェクトに変換します。

    :param record: Timesheetエンティティ
    :type record: Timesheet
    :return: 勤怠情報を表す辞書型オブジェクト
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
