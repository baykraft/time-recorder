from flask import Blueprint, request, jsonify
from flask_cors import CORS
from plugins.models import engine, BreakTime
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
from typing import List


module_api = Blueprint('break_times', __name__)
CORS(module_api)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)


@module_api.route('/<int:break_time_id>', methods=['PUT'])
def update(break_time_id):
    """
    休憩時間情報を登録します。

    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()

        year = request.json['year'] if 'year' in request.json else None
        month = request.json['month'] if 'month' in request.json else None
        customer = request.json['customer'] if 'customer' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None

        filtered: BreakTime = session.query(BreakTime).filter(
            BreakTime.break_time_id == break_time_id,
            BreakTime.user == user
        ).first()

        if filtered:
            filtered.year = year
            filtered.month = month
            filtered.customer = customer
            filtered.start_time = datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None
            filtered.end_time = datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None
            result = __break_time_to_result(filtered)
            session.commit()
            session.close()
            return jsonify({'ok': True, 'record': result}), 200
        else:
            session.commit()
            session.close()
            return jsonify({'ok': False}), 404
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('', methods=['POST'])
def create():
    """
    休憩時間情報を登録します。

    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session = Session()

        year = request.json['year'] if 'year' in request.json else None
        month = request.json['month'] if 'month' in request.json else None
        customer = request.json['customer'] if 'customer' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None

        record: BreakTime = BreakTime(
            user,
            year,
            month,
            customer,
            datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None,
            datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None)
        session.add(record)
        result = __break_time_to_result(record)
        session.commit()
        session.close()
        return jsonify({'ok': True, 'record': result}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


@module_api.route('/<int:break_time_id>', methods=['DELETE'])
def delete(break_time_id):
    """
    休憩時間情報を削除します。

    :param break_time_id: 休憩時間情報ID
    :type break_time_id: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session: Session = Session()
        record: BreakTime = session.query(BreakTime).filter(
            BreakTime.break_time_id == break_time_id,
            BreakTime.user == user
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


@module_api.route('', methods=['GET'])
def records():
    token = request.args.get('token')
    r = requests.post('https://slack.com/api/auth.test', {'token': token})
    j = json.loads(r.text)
    if j['ok']:
        user = j['user_id']
        session: Session = Session()
        break_times: List[BreakTime] = session.query(BreakTime).filter(
            BreakTime.user == user
        ).all()

        results = []
        for record in break_times:
            results.append(__break_time_to_result(record))

        session.commit()
        session.close()

        return jsonify({'ok': True, 'records': results}), 200
    else:
        return jsonify({'ok': j['ok'], 'message': j['error']}), 401


def __break_time_to_result(record: BreakTime):
    """
    BreakTimeエンティティを辞書型オブジェクトに変換します。

    :param record: BreakTimeエンティティ
    :type record: BreakTime
    :return: 休憩時間情報を表す辞書型オブジェクト
    :rtype: dict
    """
    return {
        'break_time_id': record.break_time_id,
        'year': record.year,
        'month': record.month,
        'customer': record.customer,
        'start_time': '{0:%H:%M}'.format(record.start_time) if record.start_time else None,
        'end_time': '{0:%H:%M}'.format(record.end_time) if record.end_time else None,
    }