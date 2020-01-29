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


@module_api.route('/<int:year>/<int:month>/times')
def times(year, month):
    """
    指定年月の勤怠情報を取得します。

    :param year: 年
    :type year: int
    :param month: 月
    :type month: int
    :return: {year, month, date, start, end, note}
    :rtype: json
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

        timesheets = []
        for record in records:
            timesheets.append({
                'year': record.date.year,
                'month': record.date.month,
                'date': record.date.day,
                'start': '{0:%H:%M}'.format(record.start_time) if record.start_time else None,
                'end': '{0:%H:%M}'.format(record.end_time) if record.end_time else None,
                'note': record.note
            })

        session.commit()
        session.close()

        return jsonify(timesheets)
    else:
        return jsonify(j), 401
