#!/usr/bin/env python

import os 
from dotenv import load_dotenv
load_dotenv()


# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')
    NLP_PICKLE_SQL = '''select ncit_tokenizer from test_ncit_version where active_version='Y' limit 1'''

class DevelopmentConfig(Config):
    DEBUG = True
    POSTGRESQL_HOST = 'host'
    POSTGRESQL_PORT = 'port'
    POSTGRESQL_DATABASE_NAME = 'dbname'
    POSTGRESQL_USERNAME = 'user' 
    POSTGRESQL_PASSWORD = 'password'

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    POSTGRESQL_HOST = 'host'
    POSTGRESQL_PORT = 'port'
    POSTGRESQL_DATABASE_NAME = 'dbname'
    POSTGRESQL_USERNAME = 'user'
    POSTGRESQL_PASSWORD = 'password'

class ProductionConfig(Config):
    FLASK_ENV = 'production'