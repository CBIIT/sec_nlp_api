import os
import logging
import celery
import pickle

from flask import Flask, render_template, g
from flask_socketio import SocketIO
# from flask_caching import Cache
from celery import Celery
from config import Config

from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.RESULT_BACKEND)
socketio = SocketIO()
# cache = Cache(config={'CACHE_TYPE': 'RedisCache'})


def open_pickled():
    with open("PhraseMatcher.nlp", "rb") as matcherFile:
        try:
            return pickle.load(matcherFile)
        except FileNotFoundError as err:
            raise err

global_matcher = open_pickled()

def create_app() -> Flask:
    app = Flask(__name__)

    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config['SECRET_KEY'] = 'secretjsidfjsidfjsdifjsdifj!'
    app.config.from_object(CONFIG_TYPE)

    celery.conf.update(app.config)

    register_db(app)

    register_nlp(app)

    register_globals(app)

    register_blueprints(app)

    configure_logging(app)

    register_error_handlers(app)

    configure_spacy(app)

    socketio.init_app(app)
    # cache.init_app(app)

    return app

def register_db(app):
    from app.db import init_app
    
    init_app(app)

def register_nlp(app):
    from app.nlp import init_app

    init_app(app)

def register_blueprints(app):
    from app.blueprints.main import main_blueprint
    from app.blueprints.expression_generator import expression_blueprint
    from app.blueprints.tokenizer import tokenizer_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(expression_blueprint, url_prefix='/expression_generator')
    app.register_blueprint(tokenizer_blueprint, url_prefix='/tokenizer')

def register_globals(app):
    from app.nlp import get_matcher
    @app.before_first_request
    def load_global_data():
        global some_global_name
        some_global_name = get_matcher()

def register_error_handlers(app):

    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

def configure_logging(app):

    # Deactivate the default flask logger so that log messages don't get duplicated 
    app.logger.removeHandler(default_handler)

    # Create a file handler object
    file_handler = RotatingFileHandler('flaskapp.log', maxBytes=1000000, backupCount=5)

    # Set the logging level of the file handler object so that it logs INFO and up
    file_handler.setLevel(logging.INFO)

    # Create a file formatter object
    file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')

    # Apply the file formatter object to the file handler object
    file_handler.setFormatter(file_formatter)

    # Add file handler object to the logger
    app.logger.addHandler(file_handler)

def configure_spacy(app):
    from app.nlp import init_app

    init_app(app)