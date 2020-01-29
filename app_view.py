from flask import Flask, render_template
from flask_cors import CORS

from rest import routes as rest_routes

app = Flask(__name__, static_folder='./build/static', template_folder='./build')
app.register_blueprint(rest_routes.module_api, url_prefix='/rest')
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
