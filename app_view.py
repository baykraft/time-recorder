from flask import Flask

from rest import routes as rest_routes
from views import routes as view_routes

app = Flask(__name__)
app.register_blueprint(view_routes.module_api, url_prefix='/')
app.register_blueprint(rest_routes.module_api, url_prefix='/rest')


if __name__ == '__main__':
    app.run(debug=True)
