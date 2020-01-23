from flask import Flask
from main import routes

app = Flask(__name__)
app.register_blueprint(routes.module_api)
