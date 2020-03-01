from flask import Flask, render_template
from flask_cors import CORS

from rest import time_record_routes
from rest import break_time_routes
from rest import fixed_time_routes

app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')
app.register_blueprint(time_record_routes.module_api, url_prefix='/rest/time_records')
app.register_blueprint(break_time_routes.module_api, url_prefix='/rest/break_times')
app.register_blueprint(fixed_time_routes.module_api, url_prefix='/rest/fixed_times')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
