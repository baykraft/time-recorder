from flask import request, render_template, Blueprint
import requests
import json
from views_settings import *

module_api = Blueprint('views', __name__, template_folder='templates')


@module_api.route('/')
def home():
    r = requests.get(f'https://slack.com/oauth/authorize'
                     f'?client_id={WEB_API_CLIENT_ID}'
                     f'&scope=users:read'
                     f'&redirect_uri={WEB_API_REDIRECT}')
    return r.text


@module_api.route('/auth')
def auth():
    code = request.args.get('code')
    if code is None:
        return render_template('index.html')
    else:
        r = requests.get(f'https://slack.com/api/oauth.access'
                         f'?client_id={WEB_API_CLIENT_ID}'
                         f'&client_secret={WEB_API_CLIENT_SECRET}'
                         f'&code={code}'
                         f'&redirect_uri={WEB_API_REDIRECT}')
        access_token = json.loads(r.text)['access_token']
        r = requests.get(f'https://slack.com/api/auth.test'
                         f'?token={access_token}')
        return r.text
