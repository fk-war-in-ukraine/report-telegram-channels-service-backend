from flask import Flask
from flask_cors import CORS

from .api import api


def create_app():
    app = Flask(__name__)

    CORS(app, resources=r'/api/*', origins='*', send_wildcard=True)
    app.register_blueprint(api, url_prefix='/api')

    @app.errorhandler(Exception)
    def all_exception_handler(error):
        return 'Error', 500

    return app
