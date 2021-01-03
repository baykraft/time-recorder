import datetime
import json
import logging
from typing import List

import requests
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, jsonify
from flask_cors import CORS

from plugins import jsonutils
from plugins.models import Session, TransportationExpenses

module_api = Blueprint('expenses', __name__)
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


@module_api.route('/<int:year>/<int:month>', methods=['GET'])
def records(user: str, year: int, month: int):
    """
    指定年月の交通費情報を取得します。

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
        ex_records: List[TransportationExpenses] = session.query(TransportationExpenses).filter(
            TransportationExpenses.user == user,
            TransportationExpenses.date >= datetime.date(year, month, 1),
            TransportationExpenses.date < datetime.date(year, month, 1) + relativedelta(months=1)
        ).order_by(TransportationExpenses.date)
        results = list(map(lambda r: __transportation_expenses_to_result(r), ex_records))
        return jsonify({'ok': True, 'records': results}), 200
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:tran_ex_id>', methods=['DELETE'])
def delete(user: str, tran_ex_id: int):
    """
    交通費情報を削除します。

    :param user: ユーザID
    :type user: str
    :param tran_ex_id: 交通費情報ID
    :type tran_ex_id: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        record: TransportationExpenses = session.query(TransportationExpenses).filter(
            TransportationExpenses.user == user,
            TransportationExpenses.tran_ex_id == tran_ex_id
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


@module_api.route('/<int:year>/<int:month>/<int:day>', methods=['POST'])
def create(user: str, year: int, month: int, day: int):
    """
    交通費情報を登録します。

    :param user: ユーザID
    :type user: str
    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :param day: 日
    :type day: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        customer = jsonutils.strip_to_none(request.json, 'customer')
        classification = jsonutils.strip_to_none(request.json, 'classification')
        breakdown = jsonutils.strip_to_none(request.json, 'breakdown')
        billing_address = jsonutils.strip_to_none(request.json, 'billing_address')
        expenses = jsonutils.strip_to_none(request.json, 'expenses')
        transportation = jsonutils.strip_to_none(request.json, 'transportation')
        departure = jsonutils.strip_to_none(request.json, 'departure')
        arrival = jsonutils.strip_to_none(request.json, 'arrival')

        record: TransportationExpenses = TransportationExpenses(
            user,
            datetime.date(year, month, day),
            customer,
            classification,
            breakdown,
            billing_address,
            expenses,
            transportation,
            departure,
            arrival
        )
        session.add(record)
        session.flush()
        result = __transportation_expenses_to_result(record)

        return jsonify({'ok': True, 'record': result}), 201
    except Exception as e:
        session.rollback()
        logger.error(e, exc_info=True)
    finally:
        if session.is_active:
            session.commit()
        session.close()


@module_api.route('/<int:tran_ex_id>', methods=['PUT'])
def update(user: str, tran_ex_id: int):
    """
    交通費情報を更新します。

    :param user: ユーザID
    :type user: str
    :param tran_ex_id: 交通費情報ID
    :type tran_ex_id: int
    :return: JSON形式のメッセージ
    :rtype: tuple[Any, int]
    """
    session = Session()
    try:
        year: int = jsonutils.strip_to_none(request.json, 'year')
        month: int = jsonutils.strip_to_none(request.json, 'month')
        day: int = jsonutils.strip_to_none(request.json, 'day')
        customer = jsonutils.strip_to_none(request.json, 'customer')
        classification = jsonutils.strip_to_none(request.json, 'classification')
        breakdown = jsonutils.strip_to_none(request.json, 'breakdown')
        billing_address = jsonutils.strip_to_none(request.json, 'billing_address')
        expenses = jsonutils.strip_to_none(request.json, 'expenses')
        transportation = jsonutils.strip_to_none(request.json, 'transportation')
        departure = jsonutils.strip_to_none(request.json, 'departure')
        arrival = jsonutils.strip_to_none(request.json, 'arrival')

        record: TransportationExpenses = session.query(TransportationExpenses).filter(
            TransportationExpenses.user == user,
            TransportationExpenses.tran_ex_id == tran_ex_id
        ).first()

        if record:
            record.user = user
            record.date = datetime.date(year=year, month=month, day=day)
            record.customer = customer
            record.classification = classification
            record.breakdown = breakdown
            record.billing_address = billing_address
            record.expenses = expenses
            record.transportation = transportation
            record.departure = departure
            record.arrival = arrival
            result = __transportation_expenses_to_result(record)
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


def __transportation_expenses_to_result(record: TransportationExpenses):
    """
    TransportationExpensesエンティティを辞書型オブジェクトに変換します。

    :param record: TransportationExpensesエンティティ
    :type record: TransportationExpenses
    :return: 交通費を表す辞書型オブジェクト
    :rtype: dict
    """
    return {
        'tran_ex_id': record.tran_ex_id,
        'day': record.date.day,
        'customer': record.customer,
        'classification': record.classification,
        'breakdown': record.breakdown,
        'billing_address': record.billing_address,
        'expenses': record.expenses,
        'transportation': record.transportation,
        'departure': record.departure,
        'arrival': record.arrival
    }
