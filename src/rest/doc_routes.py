from flask import Blueprint, request, jsonify, send_file
import requests
import json
import logging
from flask_cors import CORS

module_api = Blueprint('docs', __name__)
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


@module_api.route('/<string:filename>', methods=['GET'])
def download(user: str, filename: str):
    """
    指定されたファイルをダウンロードします。

    :param user: ユーザID
    :type user: str
    :param filename: ファイル名
    :type filename: str
    :return: ファイルオブジェクト
    :rtype: Any
    """
    try:
        return send_file(f'resources/{filename}', as_attachment=True)
    except Exception as e:
        logger.error(e, exc_info=True)
