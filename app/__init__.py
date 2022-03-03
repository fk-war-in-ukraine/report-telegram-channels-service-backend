from flask import Flask
from flask_cors import CORS

from .api import api


class FlaskConfig:
    NAME = 'prod'
    DEBUG = False
    SSL_REDIRECT = False


def create_app():
    app = Flask(__name__)

    app.debug = False
    app.config.from_object(FlaskConfig)

    CORS(app, resources=r'/api/*', origins='*', send_wildcard=True)
    app.register_blueprint(api, url_prefix='/api')

    @app.errorhandler(Exception)
    def all_exception_handler(error: Exception):
        print(str(error))
        return str(error), 500

    return app
