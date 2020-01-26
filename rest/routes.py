from flask import Blueprint

module_api = Blueprint('rest', __name__)


@module_api.route('/hello')
def hello():
    return 'Hello, World!'
