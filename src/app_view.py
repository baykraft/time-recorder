from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

from rest import time_record_routes
from rest import break_time_routes
from rest import fixed_time_routes
from rest import doc_routes

app = Flask(__name__, static_folder='./templates/static', template_folder='./templates')
app.register_blueprint(time_record_routes.module_api, url_prefix='/rest/time_records')
app.register_blueprint(break_time_routes.module_api, url_prefix='/rest/break_times')
app.register_blueprint(fixed_time_routes.module_api, url_prefix='/rest/fixed_times')
app.register_blueprint(doc_routes.module_api, url_prefix='/rest/docs')
CORS(app)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<string:path>')
def home(path: str):
    if -1 != path.rfind('.html'):
        return render_template(path)
    else:
        return send_from_directory('./templates', path)


if __name__ == '__main__':
    app.run(debug=True)
