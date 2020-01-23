from flask import Blueprint

module_api = Blueprint('routes', __name__)


@module_api.route('/')
def hello():
    return 'Hello, World!'
