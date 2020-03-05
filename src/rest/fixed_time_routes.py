from flask import Blueprint, request, jsonify
import requests
import json
import datetime
import logging
from flask_cors import CORS
from plugins.models import Session, FixedTime
from typing import List


module_api = Blueprint('fixed_times', __name__)
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


@module_api.route('', methods=['POST'])
def create(user: str):
    """
    所定時間情報を登録します。

    :param user: ユーザID
    :type user: str
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        year = request.json['year'] if 'year' in request.json else None
        month = request.json['month'] if 'month' in request.json else None
        customer = request.json['customer'] if 'customer' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None

        record: FixedTime = FixedTime(
            user,
            year,
            month,
            customer,
            datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None,
            datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None)
        session.add(record)
        session.flush()
        result = __fixed_time_to_result(record)

        return jsonify({'ok': True, 'record': result}), 201
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:fixed_time_id>', methods=['PUT'])
def update(user: str, fixed_time_id: int):
    """
    所定時間情報を登録します。

    :param user: ユーザID
    :type user: str
    :param fixed_time_id: 所定時間情報ID
    :type fixed_time_id: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        year = request.json['year'] if 'year' in request.json else None
        month = request.json['month'] if 'month' in request.json else None
        customer = request.json['customer'] if 'customer' in request.json else None
        start_time = request.json['start_time'] if 'start_time' in request.json else None
        end_time = request.json['end_time'] if 'end_time' in request.json else None

        filtered: FixedTime = session.query(FixedTime).filter(
            FixedTime.fixed_time_id == fixed_time_id,
            FixedTime.user == user
        ).first()

        if filtered:
            filtered.year = year
            filtered.month = month
            filtered.customer = customer
            filtered.start_time = datetime.datetime.strptime(start_time, '%H:%M').time() if start_time else None
            filtered.end_time = datetime.datetime.strptime(end_time, '%H:%M').time() if end_time else None
            result = __fixed_time_to_result(filtered)
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


@module_api.route('/<int:fixed_time_id>', methods=['DELETE'])
def delete(user: str, fixed_time_id: int):
    """
    所定時間情報を削除します。

    :param user: ユーザID
    :type user: str
    :param fixed_time_id: 所定時間情報ID
    :type fixed_time_id: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        record: FixedTime = session.query(FixedTime).filter(
            FixedTime.fixed_time_id == fixed_time_id,
            FixedTime.user == user
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


@module_api.route('/<int:year>/<int:month>', methods=['GET'])
def records(user: str, year: int, month: int):
    """
    所定時間情報リストを取得します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: 所定時間情報リスト
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        fixed_times: List[FixedTime] = session.query(FixedTime).filter(
            FixedTime.user == user,
            FixedTime.year == year,
            FixedTime.month == month
        ).all()

        results = []
        for record in fixed_times:
            results.append(__fixed_time_to_result(record))

        return jsonify({'ok': True, 'records': results}), 200
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/copy', methods=['POST'])
def copy(user: str):
    """
    指定年月の所定時間情報をコピーします。

    :param user: ユーザID
    :type user: str
    :return: コピーした所定時間情報リスト
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        from_year = request.json['from_year'] if 'from_year' in request.json else None
        from_month = request.json['from_month'] if 'from_month' in request.json else None
        to_year = request.json['to_year'] if 'to_year' in request.json else None
        to_month = request.json['to_month'] if 'to_month' in request.json else None

        fixed_times: List[FixedTime] = session.query(FixedTime).filter(
            FixedTime.user == user,
            FixedTime.year == from_year,
            FixedTime.month == from_month
        ).all()

        for fixed_time in fixed_times:
            record: FixedTime = FixedTime(
                fixed_time.user,
                to_year,
                to_month,
                fixed_time.customer,
                fixed_time.start_time,
                fixed_time.end_time
            )
            session.add(record)

        session.flush()
        fixed_times: List[FixedTime] = session.query(FixedTime).filter(
            FixedTime.user == user,
            FixedTime.year == to_year,
            FixedTime.month == to_month
        ).all()

        results = []
        for fixed_time in fixed_times:
            results.append(__fixed_time_to_result(fixed_time))

        return jsonify({'ok': True, 'records': results}), 200

    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


def __fixed_time_to_result(record: FixedTime):
    """
    FixedTimeエンティティを辞書型オブジェクトに変換します。

    :param record: FixedTimeエンティティ
    :type record: FixedTime
    :return: 所定時間情報を表す辞書型オブジェクト
    :rtype: dict
    """
    return {
        'fixed_time_id': record.fixed_time_id,
        'year': record.year,
        'month': record.month,
        'customer': record.customer,
        'start_time': '{0:%H:%M}'.format(record.start_time) if record.start_time else None,
        'end_time': '{0:%H:%M}'.format(record.end_time) if record.end_time else None,
    }
